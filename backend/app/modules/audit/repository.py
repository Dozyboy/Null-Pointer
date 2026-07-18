import sqlite3
from datetime import datetime
from pathlib import Path
from threading import RLock

from app.modules.audit.schemas import PatientActivity


class SqlitePatientActivityRepository:
    """Nhật ký chỉ được bổ sung; không cung cấp thao tác sửa hoặc xóa bản ghi."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._lock = RLock()
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS patient_activity_logs (
                    id TEXT PRIMARY KEY,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    patient_code TEXT NOT NULL,
                    encounter_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    room_code TEXT,
                    clinical_order_id TEXT,
                    reservation_id TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_patient_activity_patient_time
                ON patient_activity_logs(patient_code, occurred_at DESC)
                """
            )

    def append(self, activity: PatientActivity, idempotency_key: str) -> bool:
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO patient_activity_logs (
                    id, idempotency_key, patient_code, encounter_id,
                    activity_type, title, description, occurred_at,
                    room_code, clinical_order_id, reservation_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    activity.id,
                    idempotency_key,
                    activity.patient_code,
                    activity.encounter_id,
                    activity.activity_type.value,
                    activity.title,
                    activity.description,
                    activity.occurred_at.isoformat(),
                    activity.room_code,
                    activity.clinical_order_id,
                    activity.reservation_id,
                ),
            )
        return cursor.rowcount > 0

    def list_between(
        self,
        patient_code: str,
        start: datetime,
        end: datetime,
    ) -> list[PatientActivity]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM patient_activity_logs
                WHERE patient_code = ? AND occurred_at >= ? AND occurred_at < ?
                ORDER BY occurred_at ASC, id ASC
                """,
                (patient_code, start.isoformat(), end.isoformat()),
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: sqlite3.Row) -> PatientActivity:
        return PatientActivity(
            id=row["id"],
            patient_code=row["patient_code"],
            encounter_id=row["encounter_id"],
            activity_type=row["activity_type"],
            title=row["title"],
            description=row["description"],
            occurred_at=row["occurred_at"],
            room_code=row["room_code"],
            clinical_order_id=row["clinical_order_id"],
            reservation_id=row["reservation_id"],
        )
