from django.urls import path
from .views import VigenciaListCreateView, VigenciaDetailView

urlpatterns = [
    path('vigencias/', VigenciaListCreateView.as_view(), name='vigencia-list-create'),
    path('vigencias/<int:pk>/', VigenciaDetailView.as_view(), name='vigencia-detail'),
]
