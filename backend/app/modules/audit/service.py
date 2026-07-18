from datetime import UTC, datetime, timedelta, timezone
from uuid import uuid4

from app.modules.audit.repository import SqlitePatientActivityRepository
from app.modules.audit.schemas import PatientActivity, PatientActivityType

HOSPITAL_TIME_ZONE = timezone(timedelta(hours=7), name="Asia/Bangkok")


class PatientActivityLogService:
    def __init__(self, repository: SqlitePatientActivityRepository) -> None:
        self._repository = repository

    def record(
        self,
        *,
        idempotency_key: str,
        patient_code: str,
        encounter_id: str,
        activity_type: PatientActivityType,
        title: str,
        description: str,
        room_code: str | None = None,
        clinical_order_id: str | None = None,
        reservation_id: str | None = None,
        occurred_at: datetime | None = None,
    ) -> PatientActivity:
        activity = PatientActivity(
            id=f"ACT-{uuid4().hex.upper()}",
            patient_code=patient_code.strip().upper(),
            encounter_id=encounter_id.strip(),
            activity_type=activity_type,
            title=title.strip(),
            description=description.strip(),
            occurred_at=occurred_at or datetime.now(UTC),
            room_code=room_code,
            clinical_order_id=clinical_order_id,
            reservation_id=reservation_id,
        )
        self._repository.append(activity, idempotency_key)
        return activity

    def list_today(
        self,
        patient_code: str,
        *,
        now: datetime | None = None,
    ) -> list[PatientActivity]:
        local_now = (now or datetime.now(UTC)).astimezone(HOSPITAL_TIME_ZONE)
        local_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
        local_end = local_start + timedelta(days=1)
        return self._repository.list_between(
            patient_code.strip().upper(),
            local_start.astimezone(UTC),
            local_end.astimezone(UTC),
        )
