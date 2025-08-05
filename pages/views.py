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

from django.shortcuts import render
from contratos.models import Contrato

def home(request):
    return render(request, "pages/home.html")

def profile(request):
    return render(request, "pages/profile.html")

def updateContracts(request):
    return render(request, "pages/updateContracts.html")

def contracts(request):
    contratos = Contrato.objects.all()
    return render(request, 'pages/contracts.html', {'contratos':contratos})