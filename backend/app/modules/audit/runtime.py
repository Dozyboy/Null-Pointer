from app.core.config import get_settings
from app.modules.audit.repository import SqlitePatientActivityRepository
from app.modules.audit.service import PatientActivityLogService
from app.modules.simulation.clinical_service_repository import sqlite_path_from_url

patient_activity_repository = SqlitePatientActivityRepository(
    sqlite_path_from_url(get_settings().database_url)
)
patient_activity_service = PatientActivityLogService(patient_activity_repository)
