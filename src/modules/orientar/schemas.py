from pydantic import BaseModel
from src.modules.jobs.schemas import JobMatchResponse

class OrientationResponse(BaseModel):
    gap_percentage: int
    gap_items: list[str]
    suggested_track: str
    compatible_jobs: list[JobMatchResponse]
    confidence: float