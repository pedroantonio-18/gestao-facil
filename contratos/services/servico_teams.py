from django.conf import settings
from requests import post

def enviar_alerta_teams(contrato, vigencia, dias_restantes, contato, gestor):
    if dias_restantes > 0:
        title = f'⚠️ Alerta - Vencimento Próximo: {str(contrato)} vence em {dias_restantes} dias'
    else:
        title = f'⚠️ Alerta - Contrato Vencido: {str(contrato)} venceu'

    vigencia_atual = vigencia.vigencia_atual

    mensagem = {
        'title': title,
        'contract_number': contrato.numero_contrato,
        'entity': contrato.entidade,
        'object': contrato.objeto,
        'expire_date': vigencia_atual.strftime('%d/%m/%Y'),
        'remaining_days': f'{dias_restantes} dias',
        'responsible': f'{gestor.nome} - {contato.nome}',
    }

    try:
        post(url=settings.TEAMS_WEBHOOK, json=mensagem)
        print('Mensagem enviada com sucesso para o Teams')
    except Exception as e:
        print(f'Erro ao enviar mensagem para o Teams: {e}')
