from src.modules.saude import schemas

# Sugestões de ação por humor (versão inicial)
ACOES_POR_HUMOR = {
    'feliz': 'Que bom! Aproveite esse momento! Que tal compartilhar algo bom com alguém hoje?',
    'cansado': 'Tente descansar 10 minutos sem tela. Um chá quente também ajuda.',
    'triste': 'Que tal ouvir uma música que te acalma ou ler um capítulo de um livro?',
    'ansioso': 'Experimente respirar fundo por 1 minuto: inspire 4s, segure 4s, solte 6s.',
    'sobrecarregado': 'Escolha só UMA tarefa pra focar agora. As outras podem esperar.',
}


async def processar_checkin(
    payload: schemas.SaudeRequest,
) -> schemas.SaudeResponse:
    humor = payload.humor.lower()
    derivar_cvv = payload.nota_semanal < 4

    if derivar_cvv:
        mensagem = 'Sentimos que você não está bem. Você não está sozinho(a).'
        acao_sugerida = (
            'Conversar com o CVV (188) - disponível 24h, ligação gratuita.'
        )
        alerta = True
    else:
        mensagem = f'Olá! Vimos que você está se sentindo {humor} hoje.'
        acao_sugerida = ACOES_POR_HUMOR.get(
            humor, 'Que tal fazer uma pausa e cuidar de você agora?'
        )
        alerta = False

    return schemas.SaudeResponse(
        mensagem=mensagem,
        acao_sugerida=acao_sugerida,
        derivar_cvv=derivar_cvv,
        nota_atual=payload.nota_semanal,
        alerta=alerta,
    )
