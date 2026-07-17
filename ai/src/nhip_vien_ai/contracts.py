from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class RoutePriority(StrEnum):
    SYSTEM = "system"
    FASTEST = "fastest"
    LESS_WALK = "less_walk"
    LESS_CROWD = "less_crowd"
    ACCESSIBLE = "accessible"


class CandidateStep(BaseModel):
    service_code: str
    room_id: str
    room_name: str
    floor: str
    wait_minutes_min: int = Field(ge=0)
    wait_minutes_max: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_wait_window(self) -> "CandidateStep":
        if self.wait_minutes_max < self.wait_minutes_min:
            raise ValueError("Khoảng chờ tối đa không được nhỏ hơn tối thiểu")
        return self


class RouteCandidate(BaseModel):
    id: str
    duration_minutes_min: int = Field(ge=0)
    duration_minutes_max: int = Field(ge=0)
    distance_meters: int = Field(ge=0)
    floor_changes: int = Field(ge=0)
    is_accessible: bool
    steps: list[CandidateStep] = Field(min_length=1)


class OptimizeRoutesRequest(BaseModel):
    request_id: str
    encounter_reference: str = Field(
        description="Mã tham chiếu ẩn danh, không gửi tên bệnh nhân"
    )
    priority: RoutePriority
    required_service_codes: set[str] = Field(min_length=1)
    candidates: list[RouteCandidate] = Field(min_length=1, max_length=50)
    max_options: int = Field(default=3, ge=1, le=5)


class RankedRouteOption(BaseModel):
    candidate_id: str
    rank: int = Field(ge=1)
    score: float = Field(ge=0)
    reason_codes: list[str]


class OptimizeRoutesResponse(BaseModel):
    request_id: str
    model_version: str
    generated_at: datetime
    options: list[RankedRouteOption]
    rejected_candidate_ids: list[str]


class WaitEstimateRequest(BaseModel):
    queue_length: int = Field(ge=0)
    average_service_minutes: float = Field(gt=0, le=240)
    active_capacity: int = Field(gt=0)


class WaitEstimateResponse(BaseModel):
    wait_minutes_min: int = Field(ge=0)
    wait_minutes_max: int = Field(ge=0)
    model_version: str
