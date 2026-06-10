from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional

class CourseBase(BaseModel):
    name: str
    provider: str
    area: str
    tecnologies: list[str]
    link: HttpUrl
    is_free: bool = False

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    area: Optional[str] = None
    tecnologies: Optional[list[str]] = None
    link: Optional[HttpUrl] = None
    is_free: Optional[bool] = None

class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)