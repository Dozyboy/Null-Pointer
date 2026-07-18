import sqlite3
from dataclasses import dataclass, fields
from pathlib import Path

from app.core.config import get_settings
from app.modules.clinical_orders.entities import (
    ClinicalServiceDefinition,
    ClinicalServiceInput,
)
from app.modules.clinical_orders.service import ClinicalServiceCatalogService
from app.modules.simulation.clinical_service_fixtures import CLINICAL_SERVICE_SEEDS
from app.modules.simulation.clinical_service_repository import (
    SqliteClinicalServiceRepository,
    sqlite_path_from_url,
)
from app.modules.simulation.fixtures import ROOM_SEEDS
from app.modules.simulation.room_repository import SqliteSimulationRoomRepository


@dataclass(frozen=True, slots=True)
class StandardDataImportSummary:
    created_services: int
    updated_services: int
    unchanged_services: int
    created_rooms: int
    updated_rooms: int


def _matches_seed(
    current: ClinicalServiceDefinition,
    seed: ClinicalServiceInput,
) -> bool:
    return all(
        getattr(current, field.name) == getattr(seed, field.name)
        for field in fields(ClinicalServiceInput)
    )


def _sync_services(database_path: Path) -> tuple[int, int, int]:
    repository = SqliteClinicalServiceRepository(database_path)
    catalog = ClinicalServiceCatalogService(repository)
    created = 0
    updated = 0
    unchanged = 0

    for seed in CLINICAL_SERVICE_SEEDS:
        current = repository.get_by_code(seed.code)
        if current is None:
            catalog.create(seed)
            created += 1
        elif _matches_seed(current, seed):
            unchanged += 1
        else:
            catalog.update(seed.code, seed, expected_version=current.version)
            updated += 1

    return created, updated, unchanged


def _sync_rooms(database_path: Path) -> tuple[int, int]:
    SqliteSimulationRoomRepository(database_path)
    created = 0
    updated = 0

    with sqlite3.connect(database_path, timeout=10) as connection:
        connection.row_factory = sqlite3.Row
        for seed in ROOM_SEEDS:
            location_code = seed.location_code or seed.code
            location_owner = connection.execute(
                "SELECT code FROM simulation_rooms WHERE location_code = ?",
                (location_code,),
            ).fetchone()
            if location_owner is not None and location_owner["code"] != seed.code:
                connection.execute(
                    "UPDATE simulation_rooms SET code = ? WHERE code = ?",
                    (seed.code, location_owner["code"]),
                )

            existing = connection.execute(
                "SELECT code FROM simulation_rooms WHERE code = ?",
                (seed.code,),
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO simulation_rooms (
                        code, location_code, name, department, floor, service_type,
                        average_service_minutes, operational,
                        manual_waiting_patients, status_reason
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                    """,
                    (
                        seed.code,
                        location_code,
                        seed.name,
                        seed.department,
                        seed.floor,
                        seed.service_type,
                        seed.average_service_minutes,
                        int(seed.initially_operational),
                        (
                            None
                            if seed.initially_operational
                            else "Bảo trì thiết bị theo kịch bản demo."
                        ),
                    ),
                )
                created += 1
            else:
                connection.execute(
                    """
                    UPDATE simulation_rooms
                    SET location_code = ?, name = ?, department = ?, floor = ?,
                        service_type = ?, average_service_minutes = ?
                    WHERE code = ?
                    """,
                    (
                        location_code,
                        seed.name,
                        seed.department,
                        seed.floor,
                        seed.service_type,
                        seed.average_service_minutes,
                        seed.code,
                    ),
                )
                updated += 1

    return created, updated


def sync_standard_clinical_data(
    database_path: Path,
) -> StandardDataImportSummary:
    created_services, updated_services, unchanged_services = _sync_services(
        database_path
    )
    created_rooms, updated_rooms = _sync_rooms(database_path)
    return StandardDataImportSummary(
        created_services=created_services,
        updated_services=updated_services,
        unchanged_services=unchanged_services,
        created_rooms=created_rooms,
        updated_rooms=updated_rooms,
    )


def main() -> None:
    database_path = sqlite_path_from_url(get_settings().database_url)
    summary = sync_standard_clinical_data(database_path)
    print(summary)


if __name__ == "__main__":
    main()
