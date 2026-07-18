from app.modules.patients.repository import SqlitePatientRepository
from app.modules.patients.schemas import PatientProfile


class PatientNotFoundError(LookupError):
    pass


class PatientRegistryService:
    def __init__(self, repository: SqlitePatientRepository) -> None:
        self._repository = repository

    def seed(self, patients: list[PatientProfile]) -> None:
        self._repository.seed(patients)

    def list_patients(self) -> list[PatientProfile]:
        return self._repository.list_all()

    def get_patient(self, patient_id: str) -> PatientProfile:
        normalized_id = patient_id.strip().upper()
        patient = self._repository.get(normalized_id)
        if patient is None:
            raise PatientNotFoundError(normalized_id)
        return patient
