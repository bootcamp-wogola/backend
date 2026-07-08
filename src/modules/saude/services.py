from groq import AsyncGroq
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.models import User, HealthCheck

from src.modules.saude import schemas
from src.core.settings import get_settings

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def processar_checkin(
    payload: schemas.HealthRequest,
    current_user: User,
    session: AsyncSession,
) -> schemas.HealthResponse:
    humor = payload.humor.lower()
    refer_to_cvv = payload.weekly_score <= 2

    if refer_to_cvv:
        message = 'Sentimos que você não está bem. Você não está sozinho(a).'
        suggested_action = 'Conversar com o CVV (188) - disponível 24h, ligação gratuita.'
        alert = True
    else:
        resposta_ia = await _gerar_sugestao(humor, payload.weekly_score, payload.context)
        message = f'Olá. Vimos que você está se sentindo {humor} hoje.'
        suggested_action = resposta_ia
        alert = False

    novo_checkin = HealthCheck(
        user_id=current_user.id,
        mood=humor,
        score=payload.weekly_score,
        context=payload.context,
    )
    session.add(novo_checkin)
    await session.commit()

    return schemas.HealthResponse(
        message=message,
        suggested_action=suggested_action,
        refer_to_cvv=refer_to_cvv,
        current_score=payload.weekly_score,
        alert=alert,
    )


async def _gerar_sugestao(humor: str, nota: int, contexto: str | None) -> str:
    contexto_txt = f'Contexto adicional: {contexto}.' if contexto else ''

    prompt = (f'Você é um assistente de saúde mental empático e acolhedor do App BiT, '
              f'um app de apoio para pessoas de grupos sub-representados na tecnologia.'
              f''
              f'O usuário está se sentindo {humor} hoje e sua nota semanal é {nota}.{contexto_txt}.'
              f''
              f'Sugira UMA ação concreta, humana e acessível para ajudá-lo a se sentir melhor agora.'
              f'Pode ser: ouvir uma música, ler algo, caminhar, respirar, assistir algo, etc.'
              f'Responda em português, em no máximo 2 frases, com tom acolhedor e sem julgamentos.')

    chat = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model='llama-3.1-8b-instant',
    )

    return chat.choices[0].message.content