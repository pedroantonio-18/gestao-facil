from django.core.management.base import BaseCommand
from contratos.services.servico_email import enviar_alerta_email
from contratos.services.servico_teams import enviar_alerta_teams
from contratos.models import Vigencia
from datetime import date

class Command(BaseCommand):
    help = 'Testa o envio de email manualmente'

    def handle(self, *args, **kwargs):
        vigencias = Vigencia.contratos_proximos_do_vencimento()
        vigencia = vigencias[12]
        contrato = vigencia.contrato
        contato = contrato.contato_set.first()
        gestor = contrato.gestor_set.first()

        dias_restantes = (vigencia.vigencia_atual - date.today()).days

        destinatarios = ['pedro.antonio2@discente.ufg.br']

        enviar_alerta_email(contrato, vigencia, dias_restantes, destinatarios, 'https://www.google.com')
        enviar_alerta_teams(contrato, vigencia, dias_restantes, contato, gestor)

        self.stdout.write(self.style.SUCCESS('Teste de email enviado'))
        self.stdout.write(self.style.SUCCESS('Teste de mensagem no Teams enviado'))