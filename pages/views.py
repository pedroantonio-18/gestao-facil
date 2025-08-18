from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from contratos.models import Contrato


from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from contratos.models import Contrato


def home(request):
    numero = request.GET.get('numero', '')
    entidade = request.GET.get('entidade', '')
    documento = request.GET.get('documento', '')

    todos_contratos = Contrato.objects.all()
    paginator = Paginator(todos_contratos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contratos_filtrados = None
    if numero or entidade or documento:
        contratos_filtrados = Contrato.objects.all()
        if numero:
            contratos_filtrados = contratos_filtrados.filter(
                numero_contrato__icontains=numero
            )
        if entidade:
            contratos_filtrados = contratos_filtrados.filter(
                entidade__icontains=entidade
            )
        if documento:
            contratos_filtrados = contratos_filtrados.filter(
                cnpj_cpf__icontains=documento
            )

    # 🔎 Aqui começa a lógica das notificações
    hoje = timezone.now().date()
    limite = hoje + timedelta(days=30)

    contratos_vencidos = Contrato.objects.filter(
        vigencia__vigencia_atual__lt=hoje
    ).distinct()

    contratos_a_vencer = Contrato.objects.filter(
        vigencia__vigencia_atual__gte=hoje,
        vigencia__vigencia_atual__lte=limite
    ).distinct()

    context = {
        'page_obj': page_obj,
        'contratos_filtrados': contratos_filtrados,
        'numero': numero,
        'entidade': entidade,
        'documento': documento,
        'contratos_vencidos': contratos_vencidos,
        'contratos_a_vencer': contratos_a_vencer,
    }
    return render(request, 'pages/home.html', context)



def profile(request):
    return render(request, "pages/profile.html")


def updateContracts(request):
    search = request.GET.get('search', '')

    contratos_list = Contrato.objects.all()
    if search:
        contratos_list = contratos_list.filter(
            Q(entidade__icontains=search) |
            Q(cnpj_cpf__icontains=search) |
            Q(numero_contrato__icontains=search)
        )

    paginator = Paginator(contratos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, "pages/updateContracts.html", context)
