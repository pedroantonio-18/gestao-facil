from django.core.management.base import BaseCommand
from contratos.models import Vigencia
from datetime import date
from django.db.models import Prefetch
from services.servico_email import enviar_alerta_email

# Comando para executado pelas cron jobs e enviar emails e mensagens no Teams
class Command(BaseCommand):
    help = 'Verifica contratos com vencimento em até 6 meses e prepara notificações'

    def handle(self, *args, **kwargs):
        vigencias = Vigencia.contratos_proximos_do_vencimento()

        for vigencia in vigencias:
            contrato = vigencia.contrato

            for contato in contrato.contato_set.all():
                emails = [e.email for e in contato.email_contato_set.all()]
