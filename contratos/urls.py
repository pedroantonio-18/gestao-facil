from django.urls import path
from . import views

urlpatterns = [
    path('validar-token/<uuid:token>/', views.validar_token, name='validar_token'),
]