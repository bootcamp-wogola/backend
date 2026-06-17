from pydantic import BaseModel, ConfigDict
from typing import Optional

class JobBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    company: str
    description: str
    tech_area: str
    required_technologies: list[str] = []
    salary_range: Optional[str] = None
    location: str

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    tech_area: Optional[str] = None
    required_technologies: Optional[list[str]] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None

class JobResponse(JobBase):
    id: int

class JobMatchResponse(BaseModel):
    job_details: JobResponse
    match_percentage: int