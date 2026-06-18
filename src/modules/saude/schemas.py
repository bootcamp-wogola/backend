from pydantic import BaseModel, Field

class SaudeRequest(BaseModel):
    usuario_id: str
    humor: str
    nota_semanal: int = Field(ge=1, le=5)
    contexto: str | None = None


class SaudeResponse(BaseModel):
    mensagem: str
    acao_sugerida: str
    derivar_cvv: bool
    nota_atual: int
    alerta: bool
