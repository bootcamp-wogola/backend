<<<<<<< HEAD
from groq import AsyncGroq
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.models import User
from src.modules.jobs.models import Jobs
from src.modules.jobs.schemas import JobResponse
from fastapi import HTTPException

from src.modules.orientar import schemas
from src.core.settings import get_settings
=======
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
>>>>>>> 1018b2c9264713feca22aa07a5202c3c04b106b6

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

<<<<<<< HEAD
async def processar_orientacao(
        current_user: User,
        session: AsyncSession
) -> schemas.OrientationResponse:

    result = await session.execute(
        select(Jobs).where(Jobs.tech_area == current_user.professional_profile.tech_area)
    )

    jobs = result.scalars().all()

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail='Nenhuma vaga encontrada para sua área de atuação no momento.',
        )

    user_techs = set(current_user.professional_profile.technologies)
    results = []

    for job in jobs:
        job_techs = set(job.require_techs)
        common_techs = user_techs & job_techs

        if job_techs:
            match_percentage = int(len(common_techs) / len(job_techs) * 100)
        else:
            match_percentage = 0

        results.append({
            'job': job,
            'match_percentage': match_percentage,
            'missing_techs': list(job_techs - user_techs),
        })

    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    best_match = results[0]

    gap_percentage = 100 - best_match['match_percentage']
    gap_items = best_match['missing_techs']
    confidence = best_match['match_percentage'] / 100

    suggested_track = await _gerar_trilha(
        gap_items,
        current_user.professional_profile.tech_area,
        current_user.professional_profile.experience_level,
        best_match['match_percentage'],
    )

    compatible_jobs = []

    for item in results:
        job_response = JobResponse.model_validate(item['job'])
        job_match = schemas.JobMatchResponse(
            job_details=job_response,
            match_percentage=item['match_percentage'],
        )
        compatible_jobs.append(job_match)

    return schemas.OrientationResponse(
        gap_percentage=gap_percentage,
        gap_items=gap_items,
        suggested_track=suggested_track,
        compatible_jobs=compatible_jobs,
        confidence=confidence,

    )


async def _gerar_trilha(gap_items: list[str], tech_area: str, experience_level: str, current_match: int) -> str:
    gap_texto = ', '.join(gap_items)

    prompt = (
        f'Você é um assistente de orientação de carreira do App BiT, '
        f'um app de apoio para pessoas de grupos sub-representados na tecnologia. '
        f'O usuário atua na área de {tech_area}, tem nível de experiência {experience_level}, '
        f'atende hoje {current_match}% dos requisitos da vaga mais compatível, '
        f'e precisa desenvolver as seguintes competências: {gap_texto}. '
        f'Priorize, sempre que fizer sentido para o gap, cursos gratuitos e reconhecidos '
        f'como o Programa GEAR do Google Cloud e o Programa ONE da Oracle em parceria com a Alura. '
        f'Se nenhum desses cobrir bem o gap, sugira no máximo mais dois cursos adicionais, '
        f'preferencialmente gratuitos, atuais e em português, sem inventar nomes de curso '
        f'que você não tenha certeza de que existem. '
        f'Deixe claro que, ao concluir os cursos sugeridos, o usuário pode alcançar 100% '
        f'de compatibilidade com essa vaga. '
        f'Responda em no máximo 4 frases, de forma direta e prática.'
    )

    chat = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model='llama-3.1-8b-instant',
    )

    return chat.choices[0].message.content

=======

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
>>>>>>> 1018b2c9264713feca22aa07a5202c3c04b106b6
