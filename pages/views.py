from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def profile(request):
    return render(request, "pages/profile.html")

def updateContracts(request):  # <- NOVA função, antes você tinha "profile" duplicado
    return render(request, "pages/updateContracts.html")
