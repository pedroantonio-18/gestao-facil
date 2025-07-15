from django.core.mail import send_mail

def enviar_alerta_email(destinatario, contrato, data_validade):
    assunto = 'Contrato próximo do vencimento'
    mensagem = (
        f'O contrato "{contrato}" está com vencimento previsto para {data_validade}.\n\n'
        'Avalie a necessidade de renovação ou encerramento.'
    )

    send_mail(
        subject=assunto,
        message=mensagem,
        from_email='noreply@gestaocontratos.com',
        recipient_list=[destinatario],
        fail_silently=False,
    )