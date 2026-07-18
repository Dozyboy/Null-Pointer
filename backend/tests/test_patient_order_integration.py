from pathlib import Path

import pytest

from app.modules.clinical_orders.service import ClinicalServiceCatalogService
from app.modules.patients.fixtures import PATIENT_SEEDS
from app.modules.patients.repository import SqlitePatientRepository
from app.modules.patients.service import PatientNotFoundError, PatientRegistryService
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


def make_integrated_service(database_path: Path) -> ClinicalOrderSimulationService:
    patients = PatientRegistryService(SqlitePatientRepository(database_path))
    patients.seed(PATIENT_SEEDS)
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
        patients=patients,
    )


def make_request(patient_code: str) -> DispatchClinicalOrderRequest:
    return DispatchClinicalOrderRequest(
        patient_code=patient_code,
        patient_name="Dữ liệu gửi lên không được tin cậy",
        encounter_id="SAI-ENCOUNTER",
        doctor_name="Bác sĩ sai",
        doctor_room_code="PK-SAI",
        clinical_service_codes=["LAB-HEMA"],
        priority="fastest",
        schedule_strategy="balanced",
    )


def test_order_uses_patient_identity_from_shared_database(tmp_path: Path) -> None:
    service = make_integrated_service(tmp_path / "patient-order.db")

    result = service.dispatch(make_request("BN-02318"))

    assert result.patient_name == "Lê Ngọc Anh"
    assert result.encounter_id == "TM-2026-02318"
    assert result.doctor_name == "BS. Phạm Thu Hương"
    assert result.doctor_room_code == "PK-401"


def test_order_rejects_patient_missing_from_database(tmp_path: Path) -> None:
    service = make_integrated_service(tmp_path / "patient-order.db")

    with pytest.raises(PatientNotFoundError):
        service.dispatch(make_request("BN-KHONG-TON-TAI"))
