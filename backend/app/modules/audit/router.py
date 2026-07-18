from fastapi import APIRouter

from app.modules.audit.runtime import patient_activity_service as service
from app.modules.audit.schemas import PatientActivity

router = APIRouter(prefix="/patients", tags=["patient-activities"])


@router.get(
    "/{patient_code}/activities/today",
    response_model=list[PatientActivity],
    summary="Lấy nhật ký hoạt động thật của bệnh nhân trong ngày",
)
def get_today_activities(patient_code: str) -> list[PatientActivity]:
    return service.list_today(patient_code)
