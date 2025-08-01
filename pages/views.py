from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def profile(request):
    return render(request, "pages/profile.html")

def updateContracts(request):
    return render(request, "pages/updateContracts.html")

def contracts(request):
    return render(request, "pages/contracts.html")
