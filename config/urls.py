from django.contrib import admin
from django.urls import include, path
from pages.views import home, profile, updateContracts  # <- importa daqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('perfil/', profile, name='profile'),
    path('atualizar-contratos/', updateContracts, name='update_contracts'),
    path("__reload__/", include("django_browser_reload.urls")),
]
