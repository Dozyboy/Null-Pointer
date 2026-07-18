from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class PatientActivityType(StrEnum):
    CLINICAL_ORDER_DISPATCHED = "clinical_order_dispatched"
    ROUTE_CONFIRMED = "route_confirmed"
    SERVICE_COMPLETED = "service_completed"
    JOURNEY_COMPLETED = "journey_completed"


class PatientActivity(BaseModel):
    id: str
    patient_code: str = Field(min_length=3, max_length=40)
    encounter_id: str = Field(min_length=3, max_length=60)
    activity_type: PatientActivityType
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=2, max_length=500)
    occurred_at: datetime
    room_code: str | None = Field(default=None, max_length=40)
    clinical_order_id: str | None = Field(default=None, max_length=80)
    reservation_id: str | None = Field(default=None, max_length=80)
