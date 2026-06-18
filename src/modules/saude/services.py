from groq import AsyncGroq
from src.modules.saude import schemas
from src.core.settings import get_settings

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def processar_checkin(payload: schemas.SaudeRequest) -> schemas.SaudeResponse:
    humor = payload.humor.lower()
    derivar_cvv = payload.nota_semanal <= 2

    if derivar_cvv:
        mensagem = 'Sentimos que você não está bem. Você não está sozinho(a).'
        acao_sugerida = 'Conversar com o CVV (188) - disponível 24h, ligação gratuita.'
        alerta = True
    else:
        resposta_ia = await _gerar_sugestao(humor, payload.nota_semanal, payload.contexto)
        mensagem = f'Olá. Vimos que você está se sentindo {humor} hoje.'
        acao_sugerida = resposta_ia
        alerta = False

    return schemas.SaudeResponse(
        mensagem=mensagem,
        acao_sugerida=acao_sugerida,
        derivar_cvv=derivar_cvv,
        nota_atual=payload.nota_semanal,
        alerta=alerta,
    )
async def _gerar_sugestao(humor: str, nota: int, contexto: str | None) -> str:
    contexto_txt = f'Contexto adicional: {contexto}.' if contexto else ''

    prompt = (f'Você é um assistente de saúde mental empático e acolhedor do App BiT, '
              f'um app de apoio para pessoas de grupos sub-representados na tecnologia.'
              f''
              f'O usuário está se sentindo {humor} hoje e sua nota semanal é {nota}/10.{contexto_txt}.'
              f''
              f'Sugira UMA ação concreta, humana e acessível para ajudá-lo a se sentir melhor agora.'
              f'Pode ser: ouvir uma música, ler algo, caminhar, respirar, assistir algo, etc.'
              f'Responda em português, em no máximo 2 frases, com tom acolhedor e sem julgamentos.')

    chat = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model='llama-3.1-8b-instant',
    )

    return chat.choices[0].message.content