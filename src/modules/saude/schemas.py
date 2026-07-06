from pydantic import BaseModel, Field

class HealthRequest(BaseModel):
    humor: str
    weekly_score: int = Field(ge=1, le=5)
    context: str | None = None


class HealthResponse(BaseModel):
    message: str
    suggested_action: str
    refer_to_cvv: bool
    current_score: int
    alert: bool