from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoomSeed:
    code: str
    name: str
    department: str
    floor: str
    service_type: str
    average_service_minutes: int
    initially_operational: bool = True
    location_code: str | None = None


def _make_room_group(
    *,
    prefix: str,
    room_numbers: tuple[int, ...],
    name: str,
    department: str,
    floor_number: int,
    service_type: str,
    average_service_minutes: int,
    paused_room_numbers: tuple[int, ...] = (),
) -> tuple[RoomSeed, ...]:
    return tuple(
        RoomSeed(
            code=f"{prefix}-{room_number}",
            location_code=f"{room_number} K{floor_number}",
            name=f"{name} {room_number}",
            department=department,
            floor=f"Tầng {floor_number}",
            service_type=service_type,
            average_service_minutes=average_service_minutes,
            initially_operational=room_number not in paused_room_numbers,
        )
        for room_number in room_numbers
    )


ROOM_SEEDS = (
    *_make_room_group(
        prefix="XN",
        room_numbers=(113, 102, 103),
        name="Phòng xét nghiệm máu",
        department="Xét nghiệm",
        floor_number=1,
        service_type="blood_test",
        average_service_minutes=4,
    ),
    *_make_room_group(
        prefix="NT",
        room_numbers=(104,),
        name="Phòng nhận mẫu nước tiểu",
        department="Xét nghiệm",
        floor_number=1,
        service_type="urine_test",
        average_service_minutes=10,
    ),
    *_make_room_group(
        prefix="CT",
        room_numbers=(109, 110),
        name="Phòng CT Scanner",
        department="Chẩn đoán hình ảnh",
        floor_number=1,
        service_type="ct_scan",
        average_service_minutes=30,
    ),
    *_make_room_group(
        prefix="MRI",
        room_numbers=(111, 112),
        name="Phòng MRI chuyên sâu",
        department="Chẩn đoán hình ảnh",
        floor_number=1,
        service_type="mri",
        average_service_minutes=45,
    ),
    *_make_room_group(
        prefix="XQ",
        room_numbers=(201, 202, 203),
        name="Phòng X-quang",
        department="Chẩn đoán hình ảnh",
        floor_number=2,
        service_type="xray",
        average_service_minutes=8,
        paused_room_numbers=(202,),
    ),
    *_make_room_group(
        prefix="SA-BUNG",
        room_numbers=(204, 205, 206),
        name="Phòng siêu âm ổ bụng",
        department="Chẩn đoán hình ảnh",
        floor_number=2,
        service_type="ultrasound",
        average_service_minutes=13,
    ),
    *_make_room_group(
        prefix="SA-MEM",
        room_numbers=(208, 209),
        name="Phòng siêu âm tuyến giáp / tuyến vú / phần mềm",
        department="Chẩn đoán hình ảnh",
        floor_number=2,
        service_type="soft_tissue_ultrasound",
        average_service_minutes=10,
    ),
    *_make_room_group(
        prefix="ECG",
        room_numbers=(301, 302),
        name="Phòng điện tâm đồ / Holter",
        department="Thăm dò chức năng",
        floor_number=3,
        service_type="cardiac_monitoring",
        average_service_minutes=12,
    ),
    *_make_room_group(
        prefix="EEG",
        room_numbers=(303, 304),
        name="Phòng điện não đồ",
        department="Thăm dò chức năng",
        floor_number=3,
        service_type="eeg",
        average_service_minutes=38,
    ),
    *_make_room_group(
        prefix="ECHO",
        room_numbers=(305, 306),
        name="Phòng siêu âm tim",
        department="Tim mạch",
        floor_number=3,
        service_type="echocardiography",
        average_service_minutes=25,
    ),
    *_make_room_group(
        prefix="DOPPLER",
        room_numbers=(307, 308),
        name="Phòng siêu âm Doppler mạch máu",
        department="Tim mạch",
        floor_number=3,
        service_type="vascular_doppler",
        average_service_minutes=33,
    ),
    *_make_room_group(
        prefix="NS",
        room_numbers=(401, 402),
        name="Phòng nội soi không gây mê",
        department="Nội soi",
        floor_number=4,
        service_type="endoscopy",
        average_service_minutes=15,
    ),
    *_make_room_group(
        prefix="NS-GM",
        room_numbers=(403, 404),
        name="Phòng nội soi có gây mê",
        department="Nội soi",
        floor_number=4,
        service_type="sedated_endoscopy",
        average_service_minutes=53,
    ),
    *_make_room_group(
        prefix="HH",
        room_numbers=(405, 406),
        name="Phòng đo chức năng hô hấp",
        department="Thăm dò chức năng",
        floor_number=4,
        service_type="spirometry",
        average_service_minutes=18,
    ),
    *_make_room_group(
        prefix="NS-PQ",
        room_numbers=(407, 408),
        name="Phòng nội soi phế quản",
        department="Nội soi",
        floor_number=4,
        service_type="bronchoscopy",
        average_service_minutes=45,
    ),
    RoomSeed(
        code="PK-305",
        location_code="PK-305",
        name="Phòng khám trả kết quả",
        department="Khám chuyên khoa",
        floor="Tầng 5",
        service_type="consultation",
        average_service_minutes=12,
    ),
)


PATIENT_ROUTE_PATTERNS = (
    ("XN-113", "XQ-201", "SA-BUNG-204", "PK-305"),
    ("XN-102", "SA-BUNG-205", "PK-305"),
    ("XQ-202", "SA-BUNG-204", "PK-305"),
    ("CT-109", "PK-305"),
    ("SA-BUNG-206", "PK-305"),
)

INITIAL_PATIENT_COUNT = 24
