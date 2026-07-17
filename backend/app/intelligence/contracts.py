from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.enums import RoutePriority


class AiCandidateStep(BaseModel):
    service_code: str
    room_id: str
    room_name: str
    floor: str
    wait_minutes_min: int = Field(ge=0)
    wait_minutes_max: int = Field(ge=0)


class AiRouteCandidate(BaseModel):
    id: str
    duration_minutes_min: int = Field(ge=0)
    duration_minutes_max: int = Field(ge=0)
    distance_meters: int = Field(ge=0)
    floor_changes: int = Field(ge=0)
    is_accessible: bool
    steps: list[AiCandidateStep]


class AiOptimizeRoutesRequest(BaseModel):
    request_id: str
    encounter_reference: str
    priority: RoutePriority
    required_service_codes: set[str]
    candidates: list[AiRouteCandidate]
    max_options: int = Field(default=3, ge=1, le=5)


class AiRankedRouteOption(BaseModel):
    candidate_id: str
    rank: int
    score: float
    reason_codes: list[str]


class AiOptimizeRoutesResponse(BaseModel):
    request_id: str
    model_version: str
    generated_at: datetime
    options: list[AiRankedRouteOption]
    rejected_candidate_ids: list[str]
