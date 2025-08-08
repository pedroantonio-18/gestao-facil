from django.db import models
import uuid
from datetime import date, timedelta

class Contrato(models.Model):
    # Identificadores
    processo_sei = models.CharField(max_length=30, verbose_name='Processo SEI Formatado')
    numero_contrato = models.CharField(max_length=10, verbose_name="Contrato", primary_key=True)

    # Dados do contrato
    objeto = models.TextField(verbose_name='Objeto do Contrato')
    entidade = models.CharField(max_length=255)
    cnpj_cpf = models.CharField(max_length=30, verbose_name='CNPJ/CPF')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações sobre o Contrato')
    valor_atualizado = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Valor Atualizado do Contrato')
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('rescindido', 'Rescindido'),
        ('finalizado','Finalizado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return f'Contrato {self.numero_contrato} - {self.entidade}'

class Vigencia(models.Model):
    # Vigências
    vigencia_original = models.DateField(blank=True, null=True, verbose_name='Vigência Original')
    vigencia_atual = models.DateField(blank=True, null=True, verbose_name='Vigência Atual')
    vigencia_max = models.DateField(blank=True, null=True, verbose_name='Vigência Máxima')

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    # Calcula a vigência máxima a partir da vigência original para armazenar esse valor no banco de maneira persistente
    @property
    def calcular_vigencia_max(self):
        return self.vigencia_original + timedelta(days=5*365)
        
    # Calcula os meses restantes para o vencimento do contrato
    @property
    def proximo_ao_vencimento(self):
        if self.vigencia_atual:
            return self.vigencia_atual - date.today() <= timedelta(days=180)
        return False

    # Retorna todos os contratos que estão no período de próximo ao vencimento
    @classmethod
    def contratos_proximos_do_vencimento(cls):
        hoje = date.today()
        queryset = cls.objects.select_related('contrato').prefetch_related(
                'contrato__contato_set__email_contato_set',
                'contrato__gestor_set'
            )

        return [v for v in queryset if v.proximo_ao_vencimento and v.contrato.status == 'ativo']

    # Verifica se o contrato não pode mais ser renovado (atingiu 5 anos de vigência)
    @property
    def atingiu_vigencia_maxima(self):
        return (self.vigencia_atual - self.vigencia_original).days >= 5 * 365
    
    def __str__(self):
        return f'Contrato: {self.numero_contrato} ({self.entidade})'
    

class Contato(models.Model):
    # Dados do contato
    nome = models.CharField(blank=True, null=True, max_length=100, verbose_name='Nome')
    receber_emails = models.BooleanField(verbose_name='Deseja receber e-mails?', default=True)

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

class Telefone_Contato(models.Model):
    # Telefone do Contato
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')

    # Relações (chaves estrangeiras)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

class Email_Contato(models.Model):
    # Email do contato
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    # Relações (chaves estrangeiras)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

class Gestor(models.Model):
    # Dados do gestor
    nome = models.CharField(blank=True, null=True, max_length=100, verbose_name='Nome do Órgão Gestor')
    email = models.EmailField(blank=True, null=True, verbose_name='Email do Gestor')
    receber_emails = models.BooleanField(verbose_name='Deseja receber e-mails?', default=True)

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

class Links(models.Model):
    # Links
    link_planilhas_sei = models.URLField(blank=True, null=True, verbose_name='Link Sei para a Planilha de Custos/Preços')
    link_convencao_coletiva_sei = models.URLField(blank=True, null=True, verbose_name='Link Sei para Convenção Coletiva')

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

class Garantia(models.Model):
    # Dados da garantia
    tipo_garantia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Tipo de Garantia')
    valor_garantia = models.DecimalField(blank=True, null=True, max_digits=11, decimal_places=2, verbose_name='Valor da Garantia')

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

class Notificacao(models.Model):
    # Dados da notificação
    data_envio = models.DateField(verbose_name='Data de Envio da Notificação', blank=True, null=True)
    enviado_teams = models.BooleanField(verbose_name='Foi enviado ao Teams', default=False)

    # Relações (chaves estrangeiras)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    def __str__(self):
        return f'Notificação - Contrato {self.contrato.numero_contrato} em {self.data_envio}'

class TokenGestorNotificacao(models.Model):
    # Dados do token
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expira_em = models.DateField()
    validado = models.BooleanField(default=False)

    # Relações (chaves estrangeiras)
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE)
    gestor = models.ForeignKey(Gestor, on_delete=models.CASCADE)

    @property
    def expirado(self):
        return self.expira_em < date.today()

    def renovar(self):
        self.token = uuid.uuid4()
        self.expira_em = self.expira_em + timedelta(days=7)
        self.validado = False
        self.save()

class TokenContatoNotificacao(models.Model):
    # Dados do token
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expira_em = models.DateField()
    validado = models.BooleanField(default=False)

    # Relações (chaves estrangeiras)
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    @property
    def expirado(self):
        return self.expira_em < date.today()

    def renovar(self):
        self.token = uuid.uuid4()
        self.expira_em = self.expira_em + timedelta(days=7)
        self.validado = False
        self.save()