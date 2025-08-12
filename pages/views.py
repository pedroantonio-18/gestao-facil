from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from contratos.models import Contrato

def home(request):
    search = request.GET.get('search', '')

    # Lista completa (paginada)
    todos_contratos = Contrato.objects.all()
    paginator = Paginator(todos_contratos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lista filtrada (busca)
    contratos_filtrados = None
    if search:
        contratos_filtrados = Contrato.objects.filter(
            Q(entidade__icontains=search) |
            Q(cnpj_cpf__icontains=search) |
            Q(numero_contrato__icontains=search)
        )

    return render(request, 'pages/home.html', {
        'page_obj': page_obj,
        'search': search,
        'contratos_filtrados': contratos_filtrados,
    })

def profile(request):
    return render(request, "pages/profile.html")

def updateContracts(request):
    return render(request, "pages/updateContracts.html")


