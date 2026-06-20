from pydantic import BaseModel, Field

class OrientarResponse(BaseModel):
    gap_percentual: int = Field(..., ge=0, le=100)
    gap_itens: list[str]
    trilha_sugerida: str
    vagas_compativeis: int
    confianca: float = Field(..., ge=0.0, le=1.0)