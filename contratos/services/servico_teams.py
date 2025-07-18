from django.conf import settings
from requests import post
from datetime import datetime

def enviar_alerta_teams(contrato, vigencia, dias_restantes, contato):
    if dias_restantes > 0:
        title = f'⚠️ Alerta - Vencimento Próximo: {contrato.__str__} vence em {dias_restantes} dias'
    else:
        title = f'⚠️ Alerta - Contrato Vencido: {contrato.__str__} venceu'

    vigencia_atual = vigencia.vigencia_atual

    mensagem = {
        'title': title,
        'contract_number': contrato.numero_contrato,
        'entity': contrato.entidade,
        'expire_date': vigencia_atual.strftime('%d/%m/%Y'),
        'remaining_days': f'{dias_restantes} dias',
        'responsible': contato.nome, 
    }

    try:
        post(url=settings.TEAMS_WEBHOOK, json=mensagem)
        print('Mensagem enviada com sucesso para o Teams')
    except Exception as e:
        print('Erro ao enviar mensagem para o Teams')