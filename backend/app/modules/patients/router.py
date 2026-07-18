from fastapi import APIRouter, HTTPException, status

from app.modules.patients.runtime import patient_registry_service as service
from app.modules.patients.schemas import PatientProfile
from app.modules.patients.service import PatientNotFoundError

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get(
    "",
    response_model=list[PatientProfile],
    summary="Lấy danh sách bệnh nhân trong cơ sở dữ liệu",
)
def list_patients() -> list[PatientProfile]:
    return service.list_patients()


@router.get(
    "/{patient_id}",
    response_model=PatientProfile,
    summary="Lấy hồ sơ bệnh nhân theo mã trong QR",
)
def get_patient(patient_id: str) -> PatientProfile:
    try:
        return service.get_patient(patient_id)
    except PatientNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bệnh nhân trong cơ sở dữ liệu.",
        ) from error
