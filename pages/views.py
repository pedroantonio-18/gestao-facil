# from django.shortcuts import render
# from .models import Contrato

# def home(request):
#     return render(request, "pages/home.html")

# def profile(request):
#     return render(request, "pages/profile.html")

# def updateContracts(request):
#     return render(request, "pages/updateContracts.html")

# def contracts(request):
#     return render(request, "pages/contracts.html")

# #-----------------------------------------------------------------------------------------------------------------------#

# def contracts_view(request):
#     contratos = Contrato.objects.all()
#     return render(request, 'pages/contracts.html', {'contratos': contratos})

from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, DateField
from django.shortcuts import render
from contratos.models import Contrato, Vigencia

def home(request):
    return render(request, "pages/home.html")

def profile(request):
    return render(request, "pages/profile.html")

def updateContracts(request):
    return render(request, "pages/updateContracts.html")

def home(request):
    # Subquery para pegar a vigência_atual mais recente de cada contrato
    vigencia_subquery = Vigencia.objects.filter(
        contrato=OuterRef('pk')
    ).order_by('-vigencia_atual').values('vigencia_atual')[:1]

    contratos_recentes = Contrato.objects.annotate(
        ultima_vigencia=Subquery(vigencia_subquery, output_field=DateField())
    ).order_by('-ultima_vigencia')[:10]

    return render(request, 'pages/home.html', {'contratos_recentes': contratos_recentes})

def contracts(request):
    contratos_list = Contrato.objects.all()
    paginator = Paginator(contratos_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/contracts.html', {'page_obj': page_obj})
