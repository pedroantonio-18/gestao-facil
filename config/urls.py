from django.contrib import admin
from django.urls import include, path
from pages.views import contract, profile, updateContracts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contratos', include('contratos.urls')),
    path('perfil/', profile, name='profile'),
    path('atualizar-contratos/', updateContracts, name='update_contracts'),
    path('contract/', contract, name='contract_page'),
    
    path('', include('pages.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

