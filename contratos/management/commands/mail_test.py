from django.core.management.base import BaseCommand
from contratos.services.servico_email import enviar_alerta_email
from contratos.models import Contrato, Vigencia
from datetime import date

class Command(BaseCommand):
    help = 'Testa o envio de email manualmente'

    def handle(self, *args, **kwargs):
        vigencias = Vigencia.contratos_proximos_do_vencimento()
        vigencia = vigencias[0]
        contrato = vigencia.contrato

        dias_restantes = (vigencia.vigencia_atual - date.today()).days

        # Coloque seu próprio email de teste abaixo:
        destinatarios = ['pedro.antonio2@discente.ufg.br']

        enviar_alerta_email(contrato, vigencia, dias_restantes, destinatarios)

        self.stdout.write(self.style.SUCCESS('Teste de email enviado!'))