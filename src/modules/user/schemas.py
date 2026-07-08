from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

from src.modules.jobs.schemas import JobMatchResponse


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    birth_date: date
    gender: str
    educational_level: str
    continent: str
    country: str
    state: Optional[str] = None
    city: str
    phone_number: Optional[str] = None


class UserGet(UserBase):
    id: int
    role: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[str] = 'user'


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None


class UserList(BaseModel):
    users: list[UserGet]


class ProfessionalDataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tech_area: str
    technologies: list[str] = []
    experience_level: str
    career_goal: str


class ProfessionalDataCreate(ProfessionalDataBase):
    user_id: int


class ProfessionalDataGet(ProfessionalDataBase):
    id: int
    user_id: int

class UserGetFull(UserGet):
    professional_profile: Optional[ProfessionalDataGet] = None


class ProfessionalDataUpdate(BaseModel):
    tech_area: Optional[str] = None
    technologies: Optional[list[str]] = None
    experience_level: Optional[str] = None
    career_goal: Optional[str] = None


class HealthCheckBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mood: str = Field(...)
    score: int = Field(..., ge=1, le=5)
    context: Optional[str] = None


class HealthCheckCreate(HealthCheckBase):
    user_id: int


class HealthCheckGet(HealthCheckBase):
    id: int
    user_id: int


class HealthCheckUpdate(BaseModel):
    mood: Optional[str] = None
    score: Optional[int] = Field(None, ge=1, le=5)
    context: Optional[str] = None

