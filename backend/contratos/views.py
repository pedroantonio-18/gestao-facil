from rest_framework import generics
from contratos.models import Vigencia
from contratos.serializers import VigenciaSerializer

class VigenciaListCreateView(generics.ListCreateAPIView):
    queryset = Vigencia.objects.all()
    serializer_class = VigenciaSerializer

class VigenciaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Vigencia.objects.all()
    serializer_class = VigenciaSerializer
