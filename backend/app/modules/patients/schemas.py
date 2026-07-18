from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class PatientGender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PatientProfile(BaseModel):
    id: str = Field(min_length=3, max_length=40)
    full_name: str = Field(min_length=2, max_length=120)
    date_of_birth: date
    gender: PatientGender
    phone: str = Field(min_length=8, max_length=20)
    email: str | None = Field(default=None, max_length=120)
    national_id: str = Field(min_length=9, max_length=20)
    health_insurance_number: str = Field(min_length=8, max_length=30)
    address: str = Field(min_length=5, max_length=300)
    emergency_contact_name: str = Field(min_length=2, max_length=120)
    emergency_contact_phone: str = Field(min_length=8, max_length=20)
    blood_type: str = Field(min_length=1, max_length=5)
    allergies: list[str] = Field(default_factory=list)
    chronic_conditions: list[str] = Field(default_factory=list)
    mobility_support: bool = False
    visual_support: bool = False
    hearing_support: bool = False
    current_encounter_id: str = Field(min_length=3, max_length=60)
    attending_doctor_name: str = Field(min_length=2, max_length=120)
    doctor_room_code: str = Field(min_length=2, max_length=40)
    created_at: datetime
