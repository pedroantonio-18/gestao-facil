# models.py
from django.db import models

class Contrato(models.Model):
    numero = models.CharField(max_length=20)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato {self.numero}"