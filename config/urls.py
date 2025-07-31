from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contratos.urls')),
=======
from django.urls import include, path
from pages.views import home, profile, updateContracts  # <- importa daqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('perfil/', profile, name='profile'),
    path('atualizar-contratos/', updateContracts, name='update_contracts'),
    path("__reload__/", include("django_browser_reload.urls")),
>>>>>>> a3a37b504a7d1a63798e85a0aa9273e06d79c533
]
