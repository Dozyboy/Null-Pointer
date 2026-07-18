from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from app.modules.clinical_orders.entities import FastingPolicy, RoomServiceType
from app.modules.routing.schemas import (
    RouteProposalResponse,
    ScheduleStrategy,
    ServiceCode,
)
from app.shared.enums import RoutePriority


class ClinicalOrderStatus(StrEnum):
    ROUTED = "routed"


class DispatchClinicalOrderRequest(BaseModel):
    patient_code: str = Field(min_length=3, max_length=40)
    patient_name: str = Field(min_length=2, max_length=120)
    encounter_id: str = Field(min_length=3, max_length=60)
    doctor_name: str = Field(min_length=2, max_length=120)
    doctor_room_code: str = Field(default="PK-305", min_length=2, max_length=40)
    clinical_service_codes: list[str] = Field(min_length=1, max_length=12)
    priority: RoutePriority = RoutePriority.FASTEST
    schedule_strategy: ScheduleStrategy = ScheduleStrategy.BALANCED

    @field_validator(
        "patient_code",
        "patient_name",
        "encounter_id",
        "doctor_name",
        "doctor_room_code",
        mode="before",
    )
    @classmethod
    def strip_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("clinical_service_codes")
    @classmethod
    def validate_service_codes(cls, value: list[str]) -> list[str]:
        normalized = [code.strip().upper() for code in value if code.strip()]
        if not normalized:
            raise ValueError("Phải có ít nhất một chỉ định.")
        if len(normalized) != len(set(normalized)):
            raise ValueError("Mỗi chỉ định chỉ được gửi một lần.")
        return normalized


class RecalculateClinicalOrderRouteRequest(BaseModel):
    priority: RoutePriority = RoutePriority.FASTEST
    schedule_strategy: ScheduleStrategy = ScheduleStrategy.BALANCED
    completed_route_service_codes: list[ServiceCode] = Field(
        default_factory=list,
        max_length=15,
    )
    start_room_code: str | None = Field(default=None, min_length=2, max_length=40)

    @field_validator("completed_route_service_codes")
    @classmethod
    def validate_completed_services(
        cls,
        value: list[ServiceCode],
    ) -> list[ServiceCode]:
        if len(value) != len(set(value)):
            raise ValueError("Mỗi dịch vụ đã hoàn thành chỉ được gửi một lần.")
        if ServiceCode.DOCTOR_RETURN in value:
            raise ValueError("Không thể đánh dấu bước quay lại bác sĩ là dịch vụ đã hoàn thành.")
        return value

    @field_validator("start_room_code", mode="before")
    @classmethod
    def normalize_start_room_code(cls, value: object) -> object:
        return value.strip().upper() if isinstance(value, str) else value


class MatchedRoomResponse(BaseModel):
    code: str
    location_code: str
    name: str
    floor: str
    status: str
    waiting_patients: int = Field(ge=0)
    estimated_wait_minutes: int = Field(ge=0)


class DispatchedClinicalOrderItemResponse(BaseModel):
    service_code: str
    service_name: str
    room_service_type: RoomServiceType
    fasting_policy: FastingPolicy
    fasting_hours_min: int | None
    fasting_hours_max: int | None
    notes: str | None
    configured_room_locations: list[str]
    matched_rooms: list[MatchedRoomResponse]


class ClinicalOrderDispatchResponse(BaseModel):
    id: str
    status: ClinicalOrderStatus
    patient_code: str
    patient_name: str
    encounter_id: str
    doctor_name: str
    doctor_room_code: str
    created_at: datetime
    items: list[DispatchedClinicalOrderItemResponse]
    route_proposal: RouteProposalResponse
