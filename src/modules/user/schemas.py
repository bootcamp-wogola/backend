from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional


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
    experience_level: str
    career_goal: str


class ProfessionalDataCreate(ProfessionalDataBase):
    user_id: int


class ProfessionalDataGet(ProfessionalDataBase):
    id: int
    user_id: int


class ProfessionalDataUpdate(BaseModel):
    tech_area: Optional[str] = None
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


class OrientationResponse(BaseModel):
    gap_percentage: int
    gap_items: list[str]
    suggested_track: str
    compatible_jobs: int
    confidence: float


class HealthResponse(BaseModel):
    message: str
    suggested_action: str
    refer_to_cvv: bool
    current_score: int
    alert: bool
