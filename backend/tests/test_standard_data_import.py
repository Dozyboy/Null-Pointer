import sqlite3
from pathlib import Path

from app.modules.simulation.clinical_service_fixtures import CLINICAL_SERVICE_SEEDS
from app.modules.simulation.fixtures import ROOM_SEEDS
from app.modules.simulation.standard_data_import import sync_standard_clinical_data


def test_standard_data_import_is_idempotent(tmp_path: Path) -> None:
    database_path = tmp_path / "standard-data.db"

    sync_standard_clinical_data(database_path)
    repeated = sync_standard_clinical_data(database_path)

    with sqlite3.connect(database_path) as connection:
        service_count = connection.execute(
            "SELECT COUNT(*) FROM simulation_clinical_services"
        ).fetchone()[0]
        room_count = connection.execute(
            "SELECT COUNT(*) FROM simulation_rooms"
        ).fetchone()[0]

    assert service_count == len(CLINICAL_SERVICE_SEEDS)
    assert room_count == len(ROOM_SEEDS)
    assert repeated.unchanged_services == len(CLINICAL_SERVICE_SEEDS)
