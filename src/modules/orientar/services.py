from groq import AsyncGroq
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.models import User
from src.modules.jobs.models import Jobs
from src.modules.jobs.schemas import JobResponse
from fastapi import HTTPException

from src.modules.orientar import schemas
from src.core.settings import get_settings

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

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

