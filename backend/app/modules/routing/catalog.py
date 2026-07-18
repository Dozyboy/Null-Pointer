from dataclasses import dataclass
from enum import StrEnum

from app.modules.routing.schemas import ServiceCode


class LockedPosition(StrEnum):
    FIRST = "first"
    LAST = "last"


@dataclass(frozen=True, slots=True)
class ServiceDefinition:
    code: ServiceCode
    name: str
    room_service_type: str
    result_turnaround_minutes: int
    locked_position: LockedPosition | None = None
    lock_reason: str | None = None


SERVICE_CATALOG = {
    ServiceCode.BLOOD_TEST: ServiceDefinition(
        code=ServiceCode.BLOOD_TEST,
        name="Xét nghiệm máu",
        room_service_type="blood_test",
        result_turnaround_minutes=25,
        locked_position=LockedPosition.FIRST,
        lock_reason=(
            "Lấy máu trước để mẫu được xử lý trong lúc thực hiện các dịch vụ khác."
        ),
    ),
    ServiceCode.URINE_TEST: ServiceDefinition(
        code=ServiceCode.URINE_TEST,
        name="Nhận mẫu nước tiểu",
        room_service_type="urine_test",
        result_turnaround_minutes=45,
    ),
    ServiceCode.CHEST_XRAY: ServiceDefinition(
        code=ServiceCode.CHEST_XRAY,
        name="Chụp X-quang ngực",
        room_service_type="xray",
        result_turnaround_minutes=10,
    ),
    ServiceCode.ABDOMINAL_ULTRASOUND: ServiceDefinition(
        code=ServiceCode.ABDOMINAL_ULTRASOUND,
        name="Siêu âm bụng",
        room_service_type="ultrasound",
        result_turnaround_minutes=8,
    ),
    ServiceCode.CT_SCAN: ServiceDefinition(
        code=ServiceCode.CT_SCAN,
        name="Chụp CT",
        room_service_type="ct_scan",
        result_turnaround_minutes=15,
    ),
    ServiceCode.SOFT_TISSUE_ULTRASOUND: ServiceDefinition(
        code=ServiceCode.SOFT_TISSUE_ULTRASOUND,
        name="Siêu âm tuyến giáp / tuyến vú / phần mềm",
        room_service_type="soft_tissue_ultrasound",
        result_turnaround_minutes=0,
    ),
    ServiceCode.CARDIAC_MONITORING: ServiceDefinition(
        code=ServiceCode.CARDIAC_MONITORING,
        name="Điện tâm đồ / Holter",
        room_service_type="cardiac_monitoring",
        result_turnaround_minutes=0,
    ),
    ServiceCode.EEG: ServiceDefinition(
        code=ServiceCode.EEG,
        name="Điện não đồ",
        room_service_type="eeg",
        result_turnaround_minutes=30,
    ),
    ServiceCode.ENDOSCOPY: ServiceDefinition(
        code=ServiceCode.ENDOSCOPY,
        name="Nội soi không gây mê",
        room_service_type="endoscopy",
        result_turnaround_minutes=0,
    ),
    ServiceCode.SEDATED_ENDOSCOPY: ServiceDefinition(
        code=ServiceCode.SEDATED_ENDOSCOPY,
        name="Nội soi có gây mê",
        room_service_type="sedated_endoscopy",
        result_turnaround_minutes=0,
    ),
    ServiceCode.ECHOCARDIOGRAPHY: ServiceDefinition(
        code=ServiceCode.ECHOCARDIOGRAPHY,
        name="Siêu âm tim",
        room_service_type="echocardiography",
        result_turnaround_minutes=0,
    ),
    ServiceCode.VASCULAR_DOPPLER: ServiceDefinition(
        code=ServiceCode.VASCULAR_DOPPLER,
        name="Siêu âm Doppler mạch máu",
        room_service_type="vascular_doppler",
        result_turnaround_minutes=0,
    ),
    ServiceCode.SPIROMETRY: ServiceDefinition(
        code=ServiceCode.SPIROMETRY,
        name="Đo chức năng hô hấp",
        room_service_type="spirometry",
        result_turnaround_minutes=0,
    ),
    ServiceCode.BRONCHOSCOPY: ServiceDefinition(
        code=ServiceCode.BRONCHOSCOPY,
        name="Nội soi phế quản",
        room_service_type="bronchoscopy",
        result_turnaround_minutes=30,
    ),
    ServiceCode.MRI: ServiceDefinition(
        code=ServiceCode.MRI,
        name="Chụp MRI chuyên sâu",
        room_service_type="mri",
        result_turnaround_minutes=90,
    ),
    ServiceCode.DOCTOR_RETURN: ServiceDefinition(
        code=ServiceCode.DOCTOR_RETURN,
        name="Quay lại bác sĩ",
        room_service_type="consultation",
        result_turnaround_minutes=0,
        locked_position=LockedPosition.LAST,
        lock_reason="Chỉ quay lại bác sĩ sau khi các kết quả bắt buộc đã sẵn sàng.",
    ),
}
