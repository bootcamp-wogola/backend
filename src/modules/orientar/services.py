import json

from groq import AsyncGroq
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFound, InternalServerError
from src.core.settings import get_settings
from src.modules.user.models import User
from src.modules.user.services import get_full_user
from src.modules.jobs.services import get_matching_jobs

from .prompt import obter_prompt_orientacao
from .schemas import OrientarResponse

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def _chamar_groq(prompt: str) -> str:
    chat = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model='llama-3.3-70b-versatile',
    )
    return chat.choices[0].message.content


def _parse_resposta_ia(resposta: str) -> dict:
    try:
        return json.loads(resposta)
    except json.JSONDecodeError:
        raise InternalServerError(
            'A IA retornou um formato inválido. Tente novamente.'
        )


def _contar_vagas_compativeis(vagas: list) -> int:
    return sum(1 for item in vagas if item['match_percentage'] > 0)


async def gerar_orientacao(
    session: AsyncSession,
    current_user: User,
) -> OrientarResponse:
    full_user = await get_full_user(session, current_user)

    if not full_user or not full_user.professional_profile:
        raise NotFound(
            'Perfil profissional não encontrado. Complete seu perfil antes de continuar.'
        )

    perfil = full_user.professional_profile
    regiao = ', '.join(
        filter(None, [full_user.city, full_user.state, full_user.country])
    )

    vagas = await get_matching_jobs(
        session=session,
        user_area=perfil.tech_area,
        user_techs=perfil.technologies,
    )

    prompt = obter_prompt_orientacao(
        tech_area=perfil.tech_area,
        experience_level=perfil.experience_level,
        career_goal=perfil.career_goal,
        regiao=regiao,
        vagas=vagas,
    )

    resposta_ia = await _chamar_groq(prompt)
    dados = _parse_resposta_ia(resposta_ia)
    dados['vagas_compativeis'] = _contar_vagas_compativeis(vagas)

    try:
        return OrientarResponse(**dados)
    except ValidationError:
        print(dados)
        raise InternalServerError(
            'A IA retornou dados incompletos ou em formato inesperado. Tente novamente.'
        )
