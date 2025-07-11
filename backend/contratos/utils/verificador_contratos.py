from datetime import date, timedelta
from contratos.models import Vigencia, Gestor
from contratos.services.alerta_email import enviar_alerta_email
from contratos.services.alerta_teams import enviar_alerta_teams
from decouple import config

TEAMS_WEBHOOK_URL = config('TEAMS_WEBHOOK_URL', default='')

def verificar_contratos_vencendo():
    hoje = date.today()
    limite = hoje + timedelta(days=180) # 6 meses

    vigencias_criticas = Vigencia.objects.filter(vigencia_atual__lte=limite).select_related('contrato')

    for vigencia in vigencias_criticas:
        contrato = vigencia.contrato

        gestor = Gestor.objects.filter(contrato=contrato).first()
        if not gestor:
            continue

        if gestor.email:
            enviar_alerta_email(
                destinatario=gestor.email,
                contrato_nome=contrato.numero_contrato,
                data_validade=vigencia.vigencia_atual
            )
