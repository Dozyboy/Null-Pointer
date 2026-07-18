import sqlite3
from pathlib import Path
from threading import RLock

from app.modules.support.schemas import SupportRequestResponse


class SqliteSupportRequestRepository:
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
                CREATE TABLE IF NOT EXISTS support_requests (
                    id TEXT PRIMARY KEY,
                    encounter_id TEXT NOT NULL,
                    support_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    note TEXT,
                    status TEXT NOT NULL,
                    is_demo INTEGER NOT NULL,
                    estimated_response_minutes_min INTEGER NOT NULL,
                    estimated_response_minutes_max INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save(self, request: SupportRequestResponse) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO support_requests (
                    id, encounter_id, support_type, location, note, status,
                    is_demo, estimated_response_minutes_min,
                    estimated_response_minutes_max, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request.id,
                    request.encounter_id,
                    request.support_type.value,
                    request.location,
                    request.note,
                    request.status,
                    int(request.is_demo),
                    request.estimated_response_minutes_min,
                    request.estimated_response_minutes_max,
                    request.created_at.isoformat(),
                ),
            )

    def get_by_id(self, request_id: str) -> SupportRequestResponse | None:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM support_requests WHERE id = ?",
                (request_id,),
            ).fetchone()
        if row is None:
            return None
        return SupportRequestResponse(
            id=row["id"],
            encounter_id=row["encounter_id"],
            support_type=row["support_type"],
            location=row["location"],
            note=row["note"],
            status=row["status"],
            is_demo=bool(row["is_demo"]),
            estimated_response_minutes_min=row["estimated_response_minutes_min"],
            estimated_response_minutes_max=row["estimated_response_minutes_max"],
            created_at=row["created_at"],
        )
