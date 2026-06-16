from pydantic import BaseModel


class SaudeRequest(BaseModel):
    usuario_id: str
    humor: str
    nota_semanal: int
    contexto: str | None = None


class SaudeResponse(BaseModel):
    mensagem: str
    acao_sugerida: str
    derivar_cvv: bool
    nota_atual: int
    alerta: bool
