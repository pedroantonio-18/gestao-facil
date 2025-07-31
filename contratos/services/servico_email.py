from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def enviar_alerta_email(contrato, vigencia, dias_restantes, destinatarios_info):
    for info in destinatarios_info:
        email_destino = info['email']
        url_validacao = info['url_validacao']
        
        if dias_restantes > 0:
            assunto = f'[TRF1] Alerta: {contrato.__str__} vence em {dias_restantes} dias'
        else:
            assunto = f'[TRF1] Alerta: {contrato.__str__} venceu!'

        corpo_html = render_to_string('emails/alerta_vencimento.html', {
            'contrato': contrato,
            'vigencia': vigencia,
            'dias_restantes': dias_restantes,
            'url_validacao': url_validacao
        })

        email = EmailMessage(
            subject=assunto,
            body=corpo_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_destino],
        )
        email.content_subtype = 'html'

        try:
            email.send()
            print(f'Email enviado para: {email_destino}')
        except Exception as e:
            print(f'Erro ao enviar email para {email_destino}: {e}')
