from app.core.config import get_settings
from app.modules.patients.fixtures import PATIENT_SEEDS
from app.modules.patients.repository import SqlitePatientRepository
from app.modules.patients.service import PatientRegistryService
from app.modules.simulation.clinical_service_repository import sqlite_path_from_url

patient_repository = SqlitePatientRepository(
    sqlite_path_from_url(get_settings().database_url)
)
patient_registry_service = PatientRegistryService(patient_repository)
patient_registry_service.seed(PATIENT_SEEDS)
