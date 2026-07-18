from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.modules.audit import router as activity_router
from app.modules.audit.repository import SqlitePatientActivityRepository
from app.modules.audit.schemas import PatientActivityType
from app.modules.audit.service import PatientActivityLogService
from app.modules.reservations.repository import InMemoryRouteReservationRepository
from app.modules.reservations.schemas import (
    CreateRouteReservationRequest,
    JourneyStatus,
)
from app.modules.reservations.service import RouteReservationService
from app.modules.routing.schemas import CreateRouteProposalRequest
from app.modules.routing.service import RouteProposalService


def make_activity_service(database_path: Path) -> PatientActivityLogService:
    return PatientActivityLogService(SqlitePatientActivityRepository(database_path))


def test_activity_log_is_persistent_idempotent_and_filtered_by_today(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "activities.db"
    service = make_activity_service(database_path)
    now = datetime(2026, 7, 18, 3, 30, tzinfo=UTC)

    for _ in range(2):
        service.record(
            idempotency_key="order:001:dispatched",
            patient_code="BN-00847",
            encounter_id="TM-2026-00847",
            activity_type=PatientActivityType.CLINICAL_ORDER_DISPATCHED,
            title="Đã nhận chỉ định mới",
            description="Bác sĩ đã gửi chỉ định.",
            occurred_at=now,
        )
    service.record(
        idempotency_key="order:old:dispatched",
        patient_code="BN-00847",
        encounter_id="TM-2026-00847",
        activity_type=PatientActivityType.CLINICAL_ORDER_DISPATCHED,
        title="Chỉ định ngày trước",
        description="Bản ghi không thuộc hôm nay.",
        occurred_at=now - timedelta(days=1),
    )

    restarted_service = make_activity_service(database_path)
    activities = restarted_service.list_today("bn-00847", now=now)

    assert len(activities) == 1
    assert activities[0].title == "Đã nhận chỉ định mới"


def test_reservation_events_are_written_as_real_patient_activities(
    tmp_path: Path,
) -> None:
    activities = make_activity_service(tmp_path / "journey-activities.db")
    proposals = RouteProposalService()
    reservations = RouteReservationService(
        proposal_service=proposals,
        repository=InMemoryRouteReservationRepository(),
        activities=activities,
    )
    proposal = proposals.create_proposal(
        "TM-2026-00847",
        CreateRouteProposalRequest(),
    )
    hold = reservations.create_hold(
        CreateRouteReservationRequest(
            encounter_id=proposal.encounter_id,
            route_proposal_id=proposal.id,
            route_option_id=proposal.options[0].id,
            idempotency_key="activity-reservation-key",
            patient_code="BN-00847",
            clinical_order_id="SIM-ORDER-001",
        )
    )

    confirmed = reservations.confirm(hold.id)
    reservations.update_progress(
        confirmed.id,
        current_step=1,
        journey_status=JourneyStatus.ACTIVE,
    )
    reservations.update_progress(
        confirmed.id,
        current_step=1,
        journey_status=JourneyStatus.ACTIVE,
    )
    reservations.update_progress(
        confirmed.id,
        current_step=2,
        journey_status=JourneyStatus.COMPLETED,
    )

    events = activities.list_today("BN-00847")
    assert [event.activity_type for event in events] == [
        PatientActivityType.ROUTE_CONFIRMED,
        PatientActivityType.SERVICE_COMPLETED,
        PatientActivityType.JOURNEY_COMPLETED,
    ]


def test_activity_api_returns_database_records(tmp_path: Path, monkeypatch) -> None:
    service = make_activity_service(tmp_path / "activity-api.db")
    service.record(
        idempotency_key="api-order:001",
        patient_code="BN-02318",
        encounter_id="TM-2026-02318",
        activity_type=PatientActivityType.CLINICAL_ORDER_DISPATCHED,
        title="Đã nhận 1 chỉ định mới",
        description="Bác sĩ đã gửi xét nghiệm máu.",
    )
    monkeypatch.setattr(activity_router, "service", service)

    response = TestClient(app).get(
        "/api/v1/patients/BN-02318/activities/today"
    )

    assert response.status_code == 200
    assert response.json()[0]["activity_type"] == "clinical_order_dispatched"
