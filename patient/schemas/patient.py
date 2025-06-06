from datetime import date
from typing import Optional, ClassVar

from pydantic import BaseModel, Field, EmailStr


class ContactDetails(BaseModel):
    phone_number: str = Field(
        ...,
        pattern=r"^\+\d{1,3}\d{9,12}$",
        description="Phone number must start with +, followed by country code and digits, with no spaces.",
    )
    email: EmailStr
    address_1: str
    address_2: str


class PatientRecord(BaseModel):
    patient_id: Optional[int] = None
    first_name: str = Field(
        ..., min_length=5, description="First name must have at least 5 characters"
    )
    middle_name: Optional[str] = Field(
        ..., min_length=1, description="Middle name must have at least 1 characters"
    )
    last_name: str = Field(
        ..., min_length=5, description="Last name must have at least 5 characters"
    )
    date_of_birth: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    gender: str
    blood_type: Optional[str]
    contacts: ContactDetails
