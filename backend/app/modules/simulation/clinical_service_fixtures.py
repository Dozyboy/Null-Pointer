from app.modules.clinical_orders.entities import (
    ClinicalServiceGroup,
    ClinicalServiceInput,
    FastingPolicy,
    RoomServiceType,
    SchedulingPriority,
)


def _service(
    *,
    code: str,
    name: str,
    service_group: ClinicalServiceGroup,
    room_service_type: RoomServiceType,
    description: str,
    execution_minutes: tuple[int, int],
    turnaround_minutes: tuple[int, int],
    fasting_policy: FastingPolicy,
    scheduling_priority: SchedulingPriority,
    notes: str,
    room_locations: tuple[str, ...],
    fasting_hours: tuple[int | None, int | None] = (None, None),
) -> ClinicalServiceInput:
    return ClinicalServiceInput(
        code=code,
        name=name,
        service_group=service_group,
        room_service_type=room_service_type,
        description=description,
        execution_minutes_min=execution_minutes[0],
        execution_minutes_max=execution_minutes[1],
        turnaround_minutes_min=turnaround_minutes[0],
        turnaround_minutes_max=turnaround_minutes[1],
        fasting_policy=fasting_policy,
        fasting_hours_min=fasting_hours[0],
        fasting_hours_max=fasting_hours[1],
        scheduling_priority=scheduling_priority,
        notes=notes,
        room_locations=room_locations,
    )


CLINICAL_SERVICE_SEEDS = (
    _service(
        code="LAB-HEMA",
        name="Xét nghiệm máu",
        service_group=ClinicalServiceGroup.LABORATORY,
        room_service_type=RoomServiceType.BLOOD_TEST,
        description="Lấy mẫu máu phục vụ xét nghiệm cận lâm sàng.",
        execution_minutes=(3, 5),
        turnaround_minutes=(45, 60),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLOW_START,
        notes="Ưu tiên đưa lên đầu luồng để kích hoạt đồng hồ chờ TAT.",
        room_locations=("113 K1", "102 K1", "103 K1"),
    ),
    _service(
        code="LAB-URINE",
        name="Tổng phân tích nước tiểu",
        service_group=ClinicalServiceGroup.LABORATORY,
        room_service_type=RoomServiceType.URINE_TEST,
        description="Bệnh nhân tự lấy bệnh phẩm và trả bệnh phẩm tại phòng tiếp nhận.",
        execution_minutes=(10, 10),
        turnaround_minutes=(30, 45),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes=(
            "Có thể lồng ghép trong lúc đi vệ sinh hoặc chờ các phòng khác. "
            "Tự lấy bệnh phẩm và trả bệnh phẩm tại phòng 104."
        ),
        room_locations=("104 K1",),
    ),
    _service(
        code="IMG-XRAY",
        name="X-quang thường quy",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.XRAY,
        description="Chụp ngực, xương khớp và các chỉ định X-quang thường quy.",
        execution_minutes=(5, 10),
        turnaround_minutes=(15, 30),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes="Rất linh hoạt, có thể chèn vào bất cứ lúc rảnh nào của bệnh nhân.",
        room_locations=("201 K2", "202 K2", "203 K2"),
    ),
    _service(
        code="IMG-US-ABDOMEN",
        name="Siêu âm ổ bụng tổng quát",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.ULTRASOUND,
        description="Siêu âm khảo sát ổ bụng tổng quát.",
        execution_minutes=(10, 15),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.CONDITIONAL,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes=(
            "Cần nhịn ăn và nhịn tiểu để bàng quang căng. Nếu bệnh nhân vừa lấy mẫu "
            "nước tiểu, lùi lịch 30-45 phút để bệnh nhân uống nước."
        ),
        room_locations=("204 K2", "205 K2", "206 K2"),
    ),
    _service(
        code="IMG-US-SOFT",
        name="Siêu âm tuyến giáp / tuyến vú / phần mềm",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.SOFT_TISSUE_ULTRASOUND,
        description="Siêu âm tuyến giáp, tuyến vú hoặc phần mềm.",
        execution_minutes=(10, 10),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes="Dễ điều phối, hàng đợi thường nhanh.",
        room_locations=("208 K2", "209 K2"),
    ),
    _service(
        code="IMG-CT-NC",
        name="CT Scanner không tiêm cản quang",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.CT_SCAN,
        description="Chụp CT Scanner không sử dụng thuốc cản quang.",
        execution_minutes=(10, 15),
        turnaround_minutes=(30, 45),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes="Không có ràng buộc nhịn ăn theo bảng dữ liệu chuẩn.",
        room_locations=("109 K1", "110 K1"),
    ),
    _service(
        code="IMG-CT-CONTRAST",
        name="CT Scanner / MRI có tiêm thuốc cản quang",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.CT_SCAN,
        description="Chụp có sử dụng thuốc cản quang tại khu CT Scanner.",
        execution_minutes=(30, 45),
        turnaround_minutes=(60, 90),
        fasting_policy=FastingPolicy.REQUIRED,
        fasting_hours=(4, 6),
        scheduling_priority=SchedulingPriority.LONG_TURNAROUND,
        notes=(
            "Bắt buộc kiểm tra đã có kết quả máu Ure/Creatinine để đánh giá chức năng "
            "thận trước khi cho phép chụp."
        ),
        room_locations=("109 K1", "110 K1"),
    ),
    _service(
        code="FUNC-ECG",
        name="Điện tâm đồ (ECG)",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.CARDIAC_MONITORING,
        description="Ghi điện tâm đồ khi bệnh nhân nghỉ tại chỗ.",
        execution_minutes=(5, 10),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes="Thực hiện nhanh, các phòng thường vắng.",
        room_locations=("301 K3", "302 K3"),
    ),
    _service(
        code="FUNC-EEG",
        name="Điện não đồ (EEG)",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.EEG,
        description="Ghi điện não đồ trong phòng thăm dò chức năng.",
        execution_minutes=(30, 45),
        turnaround_minutes=(15, 30),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes="Cần phòng yên tĩnh và chiếm dụng giường trong thời gian dài.",
        room_locations=("303 K3", "304 K3"),
    ),
    _service(
        code="ENDO-GI-NO-SED",
        name="Nội soi dạ dày / đại tràng không gây mê",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.ENDOSCOPY,
        description="Nội soi tiêu hóa không sử dụng gây mê.",
        execution_minutes=(10, 20),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.REQUIRED,
        fasting_hours=(8, 8),
        scheduling_priority=SchedulingPriority.MORNING,
        notes=(
            "Phải nhịn ăn rất kỹ trên 8 giờ. Nội soi đại tràng cần thời gian chuẩn bị "
            "uống thuốc xổ."
        ),
        room_locations=("401 K4", "402 K4"),
    ),
    _service(
        code="ENDO-GI-SED",
        name="Nội soi dạ dày / đại tràng có gây mê",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.SEDATED_ENDOSCOPY,
        description="Nội soi tiêu hóa có sử dụng gây mê.",
        execution_minutes=(45, 60),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.CONDITIONAL,
        scheduling_priority=SchedulingPriority.MORNING,
        notes=(
            "Cần nhịn ăn, theo dõi tỉnh mê thêm 30 phút sau soi và bệnh nhân không được "
            "tự lái xe về."
        ),
        room_locations=("403 K4", "404 K4"),
    ),
    _service(
        code="CARD-ECHO",
        name="Siêu âm tim (Echocardiography)",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.ECHOCARDIOGRAPHY,
        description="Siêu âm khảo sát cấu trúc và chức năng tim.",
        execution_minutes=(20, 30),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes=(
            "Tốn thời gian hơn siêu âm bụng và bắt buộc do bác sĩ Tim mạch thực hiện. "
            "Chỉ điều hướng bệnh nhân đến các phòng đã cấu hình."
        ),
        room_locations=("305 K3", "306 K3"),
    ),
    _service(
        code="CARD-DOPPLER",
        name="Siêu âm Doppler mạch máu",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.VASCULAR_DOPPLER,
        description="Siêu âm Doppler mạch chi dưới hoặc động mạch cảnh.",
        execution_minutes=(20, 45),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes=(
            "Thời gian thực hiện dài. Nếu có cùng siêu âm bụng, cấp time-block dài gấp "
            "ba lần bình thường ở phòng siêu âm."
        ),
        room_locations=("307 K3", "308 K3"),
    ),
    _service(
        code="CARD-HOLTER",
        name="Đeo máy Holter điện tâm đồ / huyết áp 24 giờ",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.CARDIAC_MONITORING,
        description="Lắp máy theo dõi điện tâm đồ hoặc huyết áp liên tục 24 giờ.",
        execution_minutes=(15, 15),
        turnaround_minutes=(1440, 1440),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.LONG_TURNAROUND,
        notes=(
            "Bệnh nhân đến lắp máy, ra về sinh hoạt bình thường và hôm sau quay lại tháo "
            "máy lấy kết quả; luồng khám chuyển sang ngày hôm sau."
        ),
        room_locations=("301 K3", "302 K3"),
    ),
    _service(
        code="FUNC-SPIRO",
        name="Đo chức năng hô hấp (Spirometry)",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.SPIROMETRY,
        description="Đo lưu lượng và thể tích hô hấp bằng nghiệm pháp thổi.",
        execution_minutes=(15, 20),
        turnaround_minutes=(0, 0),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.FLEXIBLE,
        notes=(
            "Bệnh nhân phải thổi nhiều lần vào máy; có thể lấp chỗ trống trong lúc chờ "
            "kết quả xét nghiệm máu."
        ),
        room_locations=("405 K4", "406 K4"),
    ),
    _service(
        code="ENDO-BRONCH",
        name="Nội soi phế quản có/không gây mê",
        service_group=ClinicalServiceGroup.FUNCTIONAL_DIAGNOSTICS,
        room_service_type=RoomServiceType.BRONCHOSCOPY,
        description="Nội soi khảo sát đường thở và phế quản.",
        execution_minutes=(30, 60),
        turnaround_minutes=(30, 30),
        fasting_policy=FastingPolicy.CONDITIONAL,
        scheduling_priority=SchedulingPriority.MORNING,
        notes=(
            "Có nhịn ăn. Bắt buộc có xét nghiệm máu đông máu và X-quang ngực trước khi "
            "thực hiện; đây là ràng buộc ưu tiên an toàn rất cao."
        ),
        room_locations=("407 K4", "408 K4"),
    ),
    _service(
        code="IMG-MRI-ADV",
        name="Chụp MRI chuyên sâu",
        service_group=ClinicalServiceGroup.IMAGING,
        room_service_type=RoomServiceType.MRI,
        description="Chụp cộng hưởng từ sọ não hoặc cột sống.",
        execution_minutes=(30, 60),
        turnaround_minutes=(60, 90),
        fasting_policy=FastingPolicy.NOT_REQUIRED,
        scheduling_priority=SchedulingPriority.LONG_TURNAROUND,
        notes=(
            "Tiếng ồn lớn và bệnh nhân phải nằm bất động lâu. Nếu hồ sơ có chứng sợ "
            "không gian hẹp, hệ thống phải cảnh báo bác sĩ."
        ),
        room_locations=("111 K1", "112 K1"),
    ),
    _service(
        code="LAB-BIOCHEM",
        name="Sinh hóa máu cơ bản",
        service_group=ClinicalServiceGroup.LABORATORY,
        room_service_type=RoomServiceType.BLOOD_TEST,
        description="Glucose, Ure, Creatinine và men gan.",
        execution_minutes=(3, 5),
        turnaround_minutes=(60, 90),
        fasting_policy=FastingPolicy.REQUIRED,
        fasting_hours=(6, 10),
        scheduling_priority=SchedulingPriority.MORNING,
        notes=(
            "Giữ lại để cung cấp kết quả Ure/Creatinine cho kiểm tra an toàn trước khi "
            "tiêm thuốc cản quang."
        ),
        room_locations=("113 K1", "102 K1", "103 K1"),
    ),
    _service(
        code="LAB-IMMUNO",
        name="Miễn dịch / Nội tiết",
        service_group=ClinicalServiceGroup.LABORATORY,
        room_service_type=RoomServiceType.BLOOD_TEST,
        description="Hormone, tuyến giáp và dấu ấn ung thư.",
        execution_minutes=(3, 5),
        turnaround_minutes=(90, 120),
        fasting_policy=FastingPolicy.CONDITIONAL,
        scheduling_priority=SchedulingPriority.LONG_TURNAROUND,
        notes="Ưu tiên sớm vì thời gian đợi kết quả dài.",
        room_locations=("113 K1", "102 K1", "103 K1"),
    ),
)
