from django.core.management.base import BaseCommand
from contratos.models import Vigencia
from datetime import date
from django.db.models import Prefetch
from contratos.services.servico_email import enviar_alerta_email
from contratos.services.servico_teams import enviar_alerta_teams

# Comando para executado pelas cron jobs e enviar emails e mensagens no Teams
class Command(BaseCommand):
    help = 'Verifica contratos com vencimento em até 6 meses e prepara notificações'

    def handle(self, *args, **kwargs):
        vigencias = Vigencia.contratos_proximos_do_vencimento()

        for vigencia in vigencias:
            contrato = vigencia.contrato
            dias_restantes = (vigencia.vigencia_atual - date.today()).days

            for contato in contrato.contato_set.all():
                enviar_alerta_teams(contrato, vigencia, dias_restantes, contato)
