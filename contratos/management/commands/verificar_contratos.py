from django.core.management.base import BaseCommand
from contratos.models import Vigencia, Notificacao, TokenGestorNotificacao, TokenContatoNotificacao
from datetime import date, timedelta
from contratos.services.servico_email import enviar_alerta_email
from contratos.services.servico_teams import enviar_alerta_teams
from decouple import config
import uuid

class Command(BaseCommand):
    help = 'Verifica contratos com vencimento em até 6 meses e prepara notificações'

    def handle(self, *args, **kwargs):
        vigencias = Vigencia.contratos_proximos_do_vencimento()

        for vigencia in vigencias:
            contrato = vigencia.contrato

            if not contrato.gestor_set.filter(email='pedro.antonio2@discente.ufg.br').exists():
                continue

            dias_restantes = (vigencia.vigencia_atual - date.today()).days
            notificacao, _ = Notificacao.objects.get_or_create(
                contrato=contrato,
                defaults={
                    'data_envio': date.today(),
                    'enviado_teams': False
                }
            )

            lista_emails = []

            # Gestores
            for gestor in contrato.gestor_set.filter(receber_emails=True):
                if not gestor.email:
                    continue

                token, created = TokenGestorNotificacao.objects.get_or_create(
                    notificacao=notificacao,
                    gestor=gestor,
                    defaults={
                        'token': uuid.uuid4(),
                        'expira_em': date.today() + timedelta(days=7),
                        'validado': False
                    }
                )
                if not created and token.expirado:
                    token.renovar()

                lista_emails.append({
                    'email': gestor.email,
                    'url_validacao': f'{config("WEBSITE_URL")}/validar-token/{token.token}/'
                })

            # Contatos
            for contato in contrato.contato_set.filter(receber_emails=True):
                email_contato = contato.email_contato_set.first()
                if not email_contato or not email_contato.email:
                    continue

                token, created = TokenContatoNotificacao.objects.get_or_create(
                    notificacao=notificacao,
                    contato=contato,
                    defaults={
                        'token': uuid.uuid4(),
                        'expira_em': date.today() + timedelta(days=7),
                        'validado': False
                    }
                )
                if not created and token.expirado:
                    token.renovar()

                lista_emails.append({
                    'email': email_contato.email,
                    'url_validacao': f'{config("WEBSITE_URL")}/validar-token/{token.token}/'
                })

            if lista_emails:
                enviar_alerta_email(contrato, vigencia, dias_restantes, lista_emails)

            if not notificacao.enviado_teams:
                for contato in contrato.contato_set.all():
                    gestor = contrato.gestor_set.first()
                    enviar_alerta_teams(contrato, vigencia, dias_restantes, contato, gestor)

        self.stdout.write(self.style.SUCCESS('Notificações processadas com sucesso'))
