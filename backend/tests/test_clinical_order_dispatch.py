from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.clinical_orders.service import ClinicalServiceCatalogService
from app.modules.routing.service import RouteProposalService
from app.modules.simulation import clinical_order_router
from app.modules.simulation.clinical_order_repository import (
    SqliteClinicalOrderRepository,
)
from app.modules.simulation.clinical_order_schemas import (
    DispatchClinicalOrderRequest,
    RecalculateClinicalOrderRouteRequest,
)
from app.modules.simulation.clinical_order_service import (
    ClinicalOrderSimulationService,
)
from app.modules.simulation.clinical_service_fixtures import CLINICAL_SERVICE_SEEDS
from app.modules.simulation.clinical_service_repository import (
    SqliteClinicalServiceRepository,
)
from app.modules.simulation.service import HospitalSimulationService


def make_service(database_path: Path) -> ClinicalOrderSimulationService:
    catalog = ClinicalServiceCatalogService(
        SqliteClinicalServiceRepository(database_path)
    )
    catalog.seed_if_empty(CLINICAL_SERVICE_SEEDS)
    simulation = HospitalSimulationService()
    return ClinicalOrderSimulationService(
        catalog=catalog,
        simulation=simulation,
        routing=RouteProposalService(simulation=simulation),
        repository=SqliteClinicalOrderRepository(database_path),
    )


def make_request() -> DispatchClinicalOrderRequest:
    return DispatchClinicalOrderRequest(
        patient_code="BN-00847",
        patient_name="Nguyễn Thị Mai",
        encounter_id="TM-2026-00847",
        doctor_name="BS. Trần Văn Hùng",
        doctor_room_code="PK-305",
        clinical_service_codes=["LAB-HEMA", "LAB-URINE"],
        priority="fastest",
        schedule_strategy="balanced",
    )


def test_dispatch_matches_operational_rooms_and_persists_patient_order(
    tmp_path: Path,
) -> None:
    service = make_service(tmp_path / "dispatch.db")

    result = service.dispatch(make_request())
    latest = service.get_latest_for_patient("BN-00847")
    recommended = result.route_proposal.options[0]

    assert latest.id == result.id
    assert [item.service_code for item in result.items] == ["LAB-HEMA", "LAB-URINE"]
    assert {room.location_code for room in result.items[0].matched_rooms} == {
        "113 K1",
        "102 K1",
        "103 K1",
    }
    assert {room.location_code for room in result.items[1].matched_rooms} == {
        "104 K1",
    }
    assert [step.service_code for step in recommended.steps] == [
        "blood_test",
        "urine_test",
        "doctor_return",
    ]
    assert recommended.steps[0].room_code.startswith("XN-")
    assert recommended.steps[1].room_code.startswith("NT-")


@pytest.fixture
def isolated_api_service(tmp_path: Path, monkeypatch) -> ClinicalOrderSimulationService:
    service = make_service(tmp_path / "dispatch-api.db")
    monkeypatch.setattr(clinical_order_router, "service", service)
    return service


def test_dispatch_api_sends_order_that_patient_can_receive(
    isolated_api_service: ClinicalOrderSimulationService,
) -> None:
    client = TestClient(app)
    request = make_request()

    dispatch_response = client.post(
        "/api/v1/simulation/clinical-orders",
        json=request.model_dump(mode="json"),
    )
    receive_response = client.get(
        "/api/v1/simulation/patients/BN-00847/clinical-orders/latest"
    )

    assert dispatch_response.status_code == 201
    assert receive_response.status_code == 200
    assert receive_response.json()["id"] == dispatch_response.json()["id"]
    assert receive_response.json()["route_proposal"]["options"]


def test_recalculation_uses_remaining_services_and_only_commits_after_confirmation(
    tmp_path: Path,
) -> None:
    service = make_service(tmp_path / "recalculate.db")
    original = service.dispatch(make_request())

    recalculated = service.recalculate_route(
        "BN-00847",
        RecalculateClinicalOrderRouteRequest(
            schedule_strategy="leave_fast",
            completed_route_service_codes=["blood_test"],
            start_room_code=original.route_proposal.options[0].steps[0].room_code,
        ),
    )

    assert recalculated.route_proposal.id != original.route_proposal.id
    assert [
        step.service_code for step in recalculated.route_proposal.options[0].steps
    ] == ["urine_test", "doctor_return"]
    assert (
        service.get_latest_for_patient("BN-00847").route_proposal.id
        == original.route_proposal.id
    )

    service.commit_route_proposal(original.id, recalculated.route_proposal)
    committed = service.get_latest_for_patient("BN-00847")

    assert committed.route_proposal.id == recalculated.route_proposal.id
    assert "thuật toán deterministic-routing-v2" in committed.route_proposal.warnings[-1]


def test_recalculation_api_reads_current_room_state(
    isolated_api_service: ClinicalOrderSimulationService,
) -> None:
    client = TestClient(app)
    isolated_api_service.dispatch(make_request())

    response = client.post(
        "/api/v1/simulation/patients/BN-00847/clinical-orders/latest/route-proposals",
        json={
            "schedule_strategy": "finish_early",
            "completed_route_service_codes": ["blood_test"],
            "start_room_code": "XN-113",
        },
    )

    assert response.status_code == 200
    proposal = response.json()["route_proposal"]
    assert proposal["schedule_strategy"] == "finish_early"
    assert [step["service_code"] for step in proposal["options"][0]["steps"]] == [
        "urine_test",
        "doctor_return",
    ]
