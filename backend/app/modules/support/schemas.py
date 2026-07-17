from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SupportType(StrEnum):
    STAFF = "staff"
    WHEELCHAIR = "wheelchair"
    DIRECTIONS = "directions"
    VISUAL_ASSISTANCE = "visual_assistance"


class CreateSupportRequest(BaseModel):
    encounter_id: str
    support_type: SupportType
    location: str = Field(min_length=1, max_length=200)
    note: str | None = Field(default=None, max_length=500)


class SupportRequestResponse(BaseModel):
    id: str
    status: str
    is_demo: bool
    estimated_response_minutes_min: int
    estimated_response_minutes_max: int
    created_at: datetime
