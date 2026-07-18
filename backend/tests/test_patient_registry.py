from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.patients import router as patient_router
from app.modules.patients.fixtures import PATIENT_SEEDS
from app.modules.patients.repository import SqlitePatientRepository
from app.modules.patients.service import PatientNotFoundError, PatientRegistryService


def make_service(database_path: Path) -> PatientRegistryService:
    service = PatientRegistryService(SqlitePatientRepository(database_path))
    service.seed(PATIENT_SEEDS)
    return service


def test_patient_profiles_are_seeded_once_and_persisted(tmp_path: Path) -> None:
    service = make_service(tmp_path / "patients.db")
    service.seed(PATIENT_SEEDS)

    patients = service.list_patients()
    patient = service.get_patient("bn-00847")

    assert len(patients) == 6
    assert patient.full_name == "Nguyễn Thị Mai"
    assert patient.health_insurance_number == "HN40100847"
    assert patient.allergies == ["Penicillin"]


def test_patient_registry_rejects_unknown_id(tmp_path: Path) -> None:
    service = make_service(tmp_path / "patients.db")

    with pytest.raises(PatientNotFoundError):
        service.get_patient("BN-KHONG-TON-TAI")


def test_patient_api_lists_and_reads_selected_patient(
    tmp_path: Path,
    monkeypatch,
) -> None:
    service = make_service(tmp_path / "patients-api.db")
    monkeypatch.setattr(patient_router, "service", service)
    client = TestClient(app)

    list_response = client.get("/api/v1/patients")
    detail_response = client.get("/api/v1/patients/BN-02318")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 6
    assert detail_response.status_code == 200
    assert detail_response.json()["full_name"] == "Lê Ngọc Anh"
