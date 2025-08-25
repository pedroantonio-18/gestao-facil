from django import forms
from contratos.models import (
    Contrato, Vigencia, Links, Garantia, Gestor,
    Contato, EmailContato, TelefoneContato
)

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['id', 'objeto', 'entidade', 'cnpj_cpf', 'observacoes',  'valor_atualizado', 'status']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
class VigenciaForm(forms.ModelForm):
    class Meta:
        model = Vigencia
        fields = ['vigencia_original', 'vigencia_atual', 'vigencia_max']
        widgets = {
            'vigencia_original': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'vigencia_atual': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'vigencia_max': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
        
class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['link_planilhas_sei', 'link_convencao_coletiva_sei']
    
class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = ['tipo_garantia', 'valor_garantia']
        
class GestorForm(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ['nome']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome']
        
class EmailContatoForm(forms.ModelForm):
    class Meta:
        model = EmailContato
        fields = ['email']
        
class TelefoneContatoForm(forms.ModelForm):
    class Meta:
        model = TelefoneContato
        fields = ['telefone']