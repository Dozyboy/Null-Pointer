from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.shared.enums import RoutePriority


class RouteLabel(StrEnum):
    RECOMMENDED = "recommended"
    LESS_WALK = "less_walk"
    LESS_CROWD = "less_crowd"


class AccessibilityNeeds(BaseModel):
    wheelchair: bool = False
    avoid_stairs: bool = False
    visual_assistance: bool = False


class CreateRouteProposalRequest(BaseModel):
    priority: RoutePriority = RoutePriority.FASTEST
    accessibility: AccessibilityNeeds = Field(default_factory=AccessibilityNeeds)


class RouteStepResponse(BaseModel):
    id: str
    order: int = Field(ge=1)
    service_code: str
    service_name: str
    room_name: str
    floor: str
    wait_minutes_min: int = Field(ge=0)
    wait_minutes_max: int = Field(ge=0)
    is_locked: bool = False
    lock_reason: str | None = None


class RouteOptionResponse(BaseModel):
    id: str
    label: RouteLabel
    duration_minutes_min: int = Field(ge=0)
    duration_minutes_max: int = Field(ge=0)
    distance_meters: int = Field(ge=0)
    floor_changes: int = Field(ge=0)
    reason: str
    steps: list[RouteStepResponse]


class RouteProposalResponse(BaseModel):
    id: str
    encounter_id: str
    priority: RoutePriority
    is_demo: bool
    updated_at: datetime
    expires_at: datetime
    options: list[RouteOptionResponse]
