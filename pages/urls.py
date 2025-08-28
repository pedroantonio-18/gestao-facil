from django.urls import path
from .views import home, saveContact

urlpatterns = [
    path('', home, name='home'),
    path('ajax/save-contact/', saveContact, name='saveContact'),
]
