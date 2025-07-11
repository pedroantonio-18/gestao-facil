from rest_framework import serializers
from contratos.models import Vigencia
from dateutil.relativedelta import relativedelta

class VigenciaSerializer(serializers.ModelSerializer):
    anos = serializers.IntegerField(write_only=True, required=False, default=0, min_value=0)
    meses = serializers.IntegerField(write_only=True, required=False, default=0, min_value=0)
    dias = serializers.IntegerField(write_only=True, required=False, default=0, min_value=0)

    class Meta:
        model = Vigencia
        fields = ['vigencia_original', 'vigencia_atual', 'vigencia_max', 'contrato', 'anos', 'meses', 'dias']
        read_only_fields = ['vigencia_max']

    # Para requisições POST
    def create(self, data_validada):
        anos = data_validada.pop('anos', 0)
        meses = data_validada.pop('meses', 0)
        dias = data_validada.pop('dias', 0)

        vigencia = Vigencia(**data_validada)

        if vigencia.vigencia_original:
            delta = relativedelta(years=anos, months=meses, days=dias)
            vigencia.vigencia_max = vigencia.vigencia_original + delta

        vigencia.save()
        return vigencia

    # Para requisições PUT
    def update(self, instance, data_validada):
        anos = data_validada.pop('anos', 0)
        meses = data_validada.pop('meses', 0)
        dias = data_validada.pop('dias', 0)

        instance.vigencia_original = data_validada.get('vigencia_original', instance.vigencia_original)
        instance.vigencia_atual = data_validada.get('vigencia_atual', instance.vigencia_atual)
        instance.contrato = data_validada.get('contrato', instance.contrato)

        if instance.vigencia_original:
            delta = relativedelta(years=anos, months=meses, days=dias)
            instance.vigencia_max = instance.vigencia_original + delta

        instance.save()
        return instance