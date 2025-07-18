from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def enviar_alerta_email(contrato, vigencia, dias_restantes, destinatarios):
    if dias_restantes > 0:
        assunto = f'[TRF1] Alertav: {contrato.__str__} vence em {dias_restantes} dias'
    else:
        assunto = f'[TRF1] Alerta: {contrato.__str__} venceu!'

    corpo_html = render_to_string('emails/alerta_vencimento.html', {
        'contrato': contrato,
        'vigencia': vigencia,
        'dias_restantes': dias_restantes,
    })
    
    email = EmailMessage(
        subject=assunto,
        body=corpo_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios,
    )
    email.content_subtype = 'html'

    try:
        email.send()
        print(f'Email enviado para: {destinatarios}')
    except Exception as e:
        print(f'Erro ao enviar email para {destinatarios}: {e}')