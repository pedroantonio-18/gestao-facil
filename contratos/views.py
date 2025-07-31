from django.shortcuts import render
from django.utils import timezone
from contratos.models import TokenGestorNotificacao, TokenContatoNotificacao
import uuid

def validar_token(request, token):
    try:
        token_uuid = uuid.UUID(str(token))
    except ValueError:
        return render(request, 'tokens/token_invalido.html')

    token_obj = None
    tipo = None

    try:
        token_obj = TokenGestorNotificacao.objects.get(token=token_uuid)
        tipo = 'gestor'
    except TokenGestorNotificacao.DoesNotExist:
        try:
            token_obj = TokenContatoNotificacao.objects.get(token=token_uuid)
            tipo = 'contato'
        except TokenContatoNotificacao.DoesNotExist:
            return render(request, 'tokens/token_invalido.html')
        
    if token_obj.validado == True:
        return render(request, 'tokens/token_invalido.html')

    if token_obj.expirado:
        return render(request, 'tokens/token_expirado.html')

    token_obj.validado = True
    token_obj.save()

    return render(request, 'tokens/token_validado.html', {
        'tipo': tipo,
        'token': token_obj
    })
