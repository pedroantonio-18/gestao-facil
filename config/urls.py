from django.contrib import admin
from django.urls import include, path
from pages.views import home, profile, updateContracts, contracts

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('contratos', include('contratos.urls')),
    
    path('', home, name='home'),
    path('perfil/', profile, name='profile'),
    path('atualizar-contratos/', updateContracts, name='update_contracts'),
    path('contracts/', contracts, name='contracts'),
]
