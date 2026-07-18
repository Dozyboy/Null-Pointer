from pathlib import Path

from app.modules.audit.repository import SqlitePatientActivityRepository
from app.modules.audit.schemas import PatientActivityType
from app.modules.audit.service import PatientActivityLogService
from app.modules.clinical_orders.service import ClinicalServiceCatalogService
from app.modules.routing.service import RouteProposalService
from app.modules.simulation.clinical_order_repository import (
    SqliteClinicalOrderRepository,
)
from app.modules.simulation.clinical_order_schemas import DispatchClinicalOrderRequest
from app.modules.simulation.clinical_order_service import (
    ClinicalOrderSimulationService,
)
from app.modules.simulation.clinical_service_fixtures import CLINICAL_SERVICE_SEEDS
from app.modules.simulation.clinical_service_repository import (
    SqliteClinicalServiceRepository,
)
from app.modules.simulation.service import HospitalSimulationService


def test_dispatching_order_writes_real_patient_activity(tmp_path: Path) -> None:
    database_path = tmp_path / "clinical-order-activity.db"
    activity_service = PatientActivityLogService(
        SqlitePatientActivityRepository(database_path)
    )
    catalog = ClinicalServiceCatalogService(
        SqliteClinicalServiceRepository(database_path)
    )
    catalog.seed_if_empty(CLINICAL_SERVICE_SEEDS)
    simulation = HospitalSimulationService()
    service = ClinicalOrderSimulationService(
        catalog=catalog,
        simulation=simulation,
        routing=RouteProposalService(simulation=simulation),
        repository=SqliteClinicalOrderRepository(database_path),
        activities=activity_service,
    )

    result = service.dispatch(
        DispatchClinicalOrderRequest(
            patient_code="BN-00847",
            patient_name="Nguyễn Thị Mai",
            encounter_id="TM-2026-00847",
            doctor_name="BS. Trần Văn Hùng",
            doctor_room_code="PK-305",
            clinical_service_codes=["LAB-HEMA"],
            priority="fastest",
            schedule_strategy="balanced",
        )
    )

    activities = activity_service.list_today(
        result.patient_code,
        now=result.created_at,
    )

    assert len(activities) == 1
    assert activities[0].activity_type is PatientActivityType.CLINICAL_ORDER_DISPATCHED
    assert activities[0].clinical_order_id == result.id
    assert activities[0].title == "Đã nhận 1 chỉ định mới"
