from django import forms
from contratos.models import (
    Contrato, Vigencia, Links, Garantia, Gestor,
    Contato, EmailContato, TelefoneContato
)

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        # Removido 'id' dos fields, pois o Django gerencia isso automaticamente.
        fields = ['objeto', 'entidade', 'cnpj_cpf', 'observacoes',  'valor_atualizado', 'status']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO: Permite que o campo de valor fique em branco.
        self.fields['valor_atualizado'].required = False
        
class VigenciaForm(forms.ModelForm):
    class Meta:
        model = Vigencia
        # Mantido 'vigencia_max' como no seu código original.
        fields = ['vigencia_original', 'vigencia_atual', 'vigencia_max']
        widgets = {
            'vigencia_original': forms.DateInput(attrs={'type': 'date'}),
            'vigencia_atual': forms.DateInput(attrs={'type': 'date'}),
            'vigencia_max': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO: Permite que os campos de data não sejam obrigatórios.
        self.fields['vigencia_original'].required = False
        self.fields['vigencia_atual'].required = False
        self.fields['vigencia_max'].required = False
        
class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['link_planilhas_sei', 'link_convencao_coletiva_sei']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO CRÍTICA: Permite que os campos de URL fiquem em branco.
        self.fields['link_planilhas_sei'].required = False
        self.fields['link_convencao_coletiva_sei'].required = False
    
class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = ['tipo_garantia', 'valor_garantia']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO: Permite que os campos de garantia fiquem em branco.
        self.fields['tipo_garantia'].required = False
        self.fields['valor_garantia'].required = False
        
class GestorForm(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO: Permite que o nome do gestor não seja obrigatório.
        self.fields['nome'].required = False

# Os formulários abaixo não precisam de alteração para o problema atual.
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
