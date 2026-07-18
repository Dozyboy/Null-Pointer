import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.routing.catalog import SERVICE_CATALOG, ServiceDefinition
from app.modules.routing.exceptions import NoFeasibleRouteError
from app.modules.routing.optimizer import DeterministicRoutingOptimizer
from app.modules.routing.schemas import (
    CreateRouteProposalRequest,
    RouteLabel,
    ScheduleStrategy,
    ServiceCode,
)
from app.modules.routing.service import RouteProposalService
from app.modules.simulation.runtime import simulation_service
from app.modules.simulation.schemas import (
    EquipmentStatus,
    RoomSnapshot,
    RoomStatus,
)
from app.shared.enums import RoutePriority

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_shared_simulation() -> None:
    simulation_service.reset()


def test_proposal_uses_live_rooms_and_preserves_required_services() -> None:
    request = CreateRouteProposalRequest()

    proposal = RouteProposalService().create_proposal("TM-DEMO-001", request)

    assert proposal.algorithm_version == "deterministic-routing-v2"
    assert proposal.simulation_tick == 0
    assert 1 <= len(proposal.options) <= 3
    required_codes = {code.value for code in request.required_service_codes}

    for option in proposal.options:
        actual_codes = {step.service_code for step in option.steps}
        assert actual_codes == required_codes
        assert option.steps[0].service_code == ServiceCode.BLOOD_TEST
        assert option.steps[-1].service_code == ServiceCode.DOCTOR_RETURN
        assert all(step.room_code != "XQ-202" for step in option.steps)
        assert option.doctor_return_minutes is not None
        assert option.doctor_return_minutes >= option.results_ready_minutes


def test_pausing_selected_room_recalculates_all_options() -> None:
    simulation_service.set_room_operation("XQ-202", operational=True, reason=None)
    service = RouteProposalService()
    request = CreateRouteProposalRequest()
    before = service.create_proposal("TM-DEMO-002", request)
    selected_xray_room = next(
        step.room_code
        for step in before.options[0].steps
        if step.service_code == ServiceCode.CHEST_XRAY
    )

    simulation_service.set_room_operation(
        selected_xray_room,
        operational=False,
        reason="Giả lập thiết bị hỏng.",
    )
    after = service.create_proposal("TM-DEMO-002", request)

    assert all(
        step.room_code != selected_xray_room
        for option in after.options
        for step in option.steps
    )


def test_no_active_room_for_required_service_fails_closed() -> None:
    xray_room_codes = [
        room.code
        for room in simulation_service.get_snapshot().rooms
        if room.service_type == "xray"
    ]
    for room_code in xray_room_codes:
        simulation_service.set_room_operation(
            room_code,
            operational=False,
            reason="Giả lập thiết bị hỏng.",
        )

    with pytest.raises(NoFeasibleRouteError, match="Chụp X-quang ngực"):
        RouteProposalService().create_proposal(
            "TM-DEMO-003",
            CreateRouteProposalRequest(),
        )


def test_priority_and_schedule_strategy_are_applied_to_recommended_option() -> None:
    request = CreateRouteProposalRequest(
        priority=RoutePriority.LESS_WALK,
        schedule_strategy=ScheduleStrategy.FINISH_EARLY,
    )

    proposal = RouteProposalService().create_proposal("TM-DEMO-004", request)

    assert proposal.priority == RoutePriority.LESS_WALK
    assert proposal.schedule_strategy == ScheduleStrategy.FINISH_EARLY
    assert proposal.options[0].label == RouteLabel.RECOMMENDED
    assert "dịch vụ" in proposal.options[0].reason.lower()


def test_subset_of_services_is_not_extended_by_algorithm() -> None:
    request = CreateRouteProposalRequest(
        required_service_codes=[
            ServiceCode.BLOOD_TEST,
            ServiceCode.CHEST_XRAY,
        ]
    )

    proposal = RouteProposalService().create_proposal("TM-DEMO-005", request)

    for option in proposal.options:
        assert [step.service_code for step in option.steps] == [
            ServiceCode.BLOOD_TEST,
            ServiceCode.CHEST_XRAY,
        ]


def test_api_rejects_unknown_or_duplicate_service_codes() -> None:
    unknown = client.post(
        "/api/v1/encounters/TM-DEMO-006/route-proposals",
        json={"required_service_codes": ["unknown_service"]},
    )
    duplicate = client.post(
        "/api/v1/encounters/TM-DEMO-006/route-proposals",
        json={"required_service_codes": ["blood_test", "blood_test"]},
    )

    assert unknown.status_code == 422
    assert duplicate.status_code == 422


def test_api_returns_conflict_instead_of_unsafe_partial_route() -> None:
    xray_room_codes = [
        room.code
        for room in simulation_service.get_snapshot().rooms
        if room.service_type == "xray"
    ]
    for room_code in xray_room_codes:
        simulation_service.set_room_operation(
            room_code,
            operational=False,
            reason="Giả lập thiết bị hỏng.",
        )

    response = client.post(
        "/api/v1/encounters/TM-DEMO-007/route-proposals",
        json={"required_service_codes": ["chest_xray"]},
    )

    assert response.status_code == 409
    assert "không có phòng" in response.json()["detail"].lower()


def test_proposal_records_current_simulation_tick() -> None:
    simulation_service.advance(5)

    proposal = RouteProposalService().create_proposal(
        "TM-DEMO-008",
        CreateRouteProposalRequest(),
    )

    assert proposal.simulation_tick == 1


def test_room_queue_and_wait_time_change_the_selected_room() -> None:
    for room_code in ("XQ-201", "XQ-202", "XQ-203"):
        simulation_service.set_room_operation(room_code, operational=True, reason=None)
        simulation_service.adjust_room_queue(room_code, -50)
    simulation_service.adjust_room_queue("XQ-201", 8)
    simulation_service.adjust_room_queue("XQ-203", 4)

    service = RouteProposalService()
    request = CreateRouteProposalRequest(
        required_service_codes=[ServiceCode.CHEST_XRAY],
        schedule_strategy=ScheduleStrategy.BALANCED,
    )
    before = service.create_proposal("TM-QUEUE-001", request)

    assert before.options[0].steps[0].room_code == "XQ-202"

    simulation_service.adjust_room_queue("XQ-202", 12)
    simulation_service.adjust_room_queue("XQ-201", -50)
    after = service.create_proposal("TM-QUEUE-001", request)

    assert after.options[0].steps[0].room_code == "XQ-201"
    assert after.options[0].total_wait_minutes < before.options[0].duration_minutes_max


def test_schedule_strategies_optimize_different_completion_targets() -> None:
    base_snapshot = simulation_service.get_snapshot()
    now = base_snapshot.simulation_time

    def room(
        code: str,
        name: str,
        floor: str,
        service_type: str,
    ) -> RoomSnapshot:
        return RoomSnapshot(
            code=code,
            location_code=code,
            name=name,
            department="Kiểm thử điều phối",
            floor=floor,
            service_type=service_type,
            status=RoomStatus.AVAILABLE,
            equipment_status=EquipmentStatus.OPERATIONAL,
            waiting_patients=0,
            waiting_patient_codes=[],
            current_patient_code=None,
            average_service_minutes=5,
            estimated_wait_minutes=0,
            status_reason=None,
            updated_at=now,
        )

    snapshot = base_snapshot.model_copy(
        update={
            "rooms": [
                room("PK-201", "Phòng bác sĩ", "Tầng 2", "consultation"),
                room("NT-202", "Phòng xét nghiệm gần", "Tầng 2", "urine_test"),
                room("XQ-501", "Phòng trả kết quả lâu", "Tầng 5", "xray"),
            ]
        }
    )
    catalog = {
        ServiceCode.URINE_TEST: ServiceDefinition(
            code=ServiceCode.URINE_TEST,
            name="Dịch vụ có thể làm ngay",
            room_service_type="urine_test",
            result_turnaround_minutes=0,
        ),
        ServiceCode.CHEST_XRAY: ServiceDefinition(
            code=ServiceCode.CHEST_XRAY,
            name="Dịch vụ trả kết quả lâu",
            room_service_type="xray",
            result_turnaround_minutes=100,
        ),
        ServiceCode.DOCTOR_RETURN: SERVICE_CATALOG[ServiceCode.DOCTOR_RETURN],
    }
    optimizer = DeterministicRoutingOptimizer()

    finish_early = optimizer.optimize(
        snapshot,
        CreateRouteProposalRequest(
            schedule_strategy=ScheduleStrategy.FINISH_EARLY,
            required_service_codes=[
                ServiceCode.CHEST_XRAY,
                ServiceCode.URINE_TEST,
                ServiceCode.DOCTOR_RETURN,
            ],
            start_room_code="PK-201",
        ),
        service_catalog=catalog,
    )[0].candidate
    doctor_ready = optimizer.optimize(
        snapshot,
        CreateRouteProposalRequest(
            schedule_strategy=ScheduleStrategy.LEAVE_FAST,
            required_service_codes=[
                ServiceCode.CHEST_XRAY,
                ServiceCode.URINE_TEST,
                ServiceCode.DOCTOR_RETURN,
            ],
            start_room_code="PK-201",
        ),
        service_catalog=catalog,
    )[0].candidate

    assert finish_early.steps[0].service.code == ServiceCode.URINE_TEST
    assert doctor_ready.steps[0].service.code == ServiceCode.CHEST_XRAY
    assert finish_early.tests_completed_minutes < doctor_ready.tests_completed_minutes
    assert doctor_ready.doctor_return_minutes < finish_early.doctor_return_minutes
