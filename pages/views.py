from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from contratos.models import (
    Contrato, Vigencia, Links, Garantia, Gestor, Contato, EmailContato, TelefoneContato
)
from datetime import timedelta
from .forms import (
    ContratoForm, VigenciaForm, LinksForm, GarantiaForm, GestorForm, ContatoForm, EmailContatoForm, TelefoneContatoForm
)
import re
import logging

logger = logging.getLogger(__name__)

def home(request):
    numero = request.GET.get('numero', '')
    entidade = request.GET.get('entidade', '')
    documento = request.GET.get('documento', '')

    todos_contratos = Contrato.objects.all().order_by('numero_contrato')
    paginator = Paginator(todos_contratos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contratos_filtrados = None
    if numero or entidade or documento:
        contratos_filtrados = Contrato.objects.all()
        if numero:
            contratos_filtrados = contratos_filtrados.filter(numero_contrato__icontains=numero)
        if entidade:
            contratos_filtrados = contratos_filtrados.filter(entidade__icontains=entidade)
        if documento:
            contratos_filtrados = contratos_filtrados.filter(cnpj_cpf__icontains=documento)

    hoje = timezone.now().date()
    limite = hoje + timedelta(days=30)

    contratos_vencidos = Contrato.objects.filter(vigencia__vigencia_atual__lt=hoje).distinct()
    contratos_a_vencer = Contrato.objects.filter(
        vigencia__vigencia_atual__gte=hoje,
        vigencia__vigencia_atual__lte=limite
    ).distinct()

    if request.method == 'POST':
        contrato_id = request.POST.get('contrato_id')
        
        # Obter o contrato
        try:
            contrato = Contrato.objects.get(id=contrato_id)
        except Contrato.DoesNotExist:
            return redirect('home')
        
        # Processar formulários principais
        _processar_formularios_principais(request, contrato)
        
        # Processar contatos existentes
        _processar_contatos_existentes(request, contrato)
        
        # Processar novos contatos
        _processar_novos_contatos(request, contrato)
            
        return redirect('home')

    # Criar forms individuais para cada contrato
    forms = []
    for contrato in page_obj:
        form_dict = _criar_forms_contrato(contrato)
        forms.append((contrato, form_dict))

    context = {
        'page_obj': page_obj,
        'contratos_filtrados': contratos_filtrados,
        'numero': numero,
        'entidade': entidade,
        'documento': documento,
        'contratos_vencidos': contratos_vencidos,
        'contratos_a_vencer': contratos_a_vencer,
        'forms': forms
    }

    return render(request, 'pages/home.html', context)


def _processar_formularios_principais(request, contrato):
    """Processa os formulários principais do contrato (contrato, vigência, links, garantia, gestor)"""
    
    # Obter ou criar instâncias relacionadas
    try:
        vigencia = Vigencia.objects.get(contrato=contrato)
    except Vigencia.DoesNotExist:
        vigencia = None
        
    try:
        links = Links.objects.get(contrato=contrato)
    except Links.DoesNotExist:
        links = None
        
    try:
        garantia = Garantia.objects.get(contrato=contrato)
    except Garantia.DoesNotExist:
        garantia = None
        
    try:
        gestor = Gestor.objects.get(contrato=contrato)
    except Gestor.DoesNotExist:
        gestor = None
    
    # Criar e validar forms com prefixos únicos
    contrato_form = ContratoForm(request.POST, instance=contrato, prefix='contrato')
    if contrato_form.is_valid():
        contrato_form.save()
    
    if vigencia:
        vigencia_form = VigenciaForm(request.POST, instance=vigencia, prefix='vigencia')
        if vigencia_form.is_valid():
            vigencia_form.save()
            
    if links:
        links_form = LinksForm(request.POST, instance=links, prefix='links')
        if links_form.is_valid():
            links_form.save()
            
    if garantia:
        garantia_form = GarantiaForm(request.POST, instance=garantia, prefix='garantia')
        if garantia_form.is_valid():
            garantia_form.save()
            
    if gestor:
        gestor_form = GestorForm(request.POST, instance=gestor, prefix='gestor')
        if gestor_form.is_valid():
            gestor_form.save()


def _processar_contatos_existentes(request, contrato):
    """Processa contatos existentes e seus emails/telefones"""
    
    # Padrões para identificar campos de contatos existentes
    contato_nome_pattern = re.compile(r'contato_nome_(\d+)_(\d+)')
    email_pattern = re.compile(r'email_contato_(\d+)_(\d+)_(\d+)')
    telefone_pattern = re.compile(r'telefone_contato_(\d+)_(\d+)_(\d+)')
    
    # Processar nomes de contatos
    contatos_processados = set()
    for field_name, value in request.POST.items():
        match = contato_nome_pattern.match(field_name)
        if match:
            contrato_id, contato_id = match.groups()
            if int(contrato_id) == contrato.id:
                try:
                    contato = Contato.objects.get(id=contato_id, contrato=contrato)
                    contato.nome = value
                    contato.save()
                    contatos_processados.add(contato_id)
                except Contato.DoesNotExist:
                    continue
    
    # Processar emails
    emails_processados = {}
    for field_name, value in request.POST.items():
        match = email_pattern.match(field_name)
        if match:
            contrato_id, contato_id, email_index = match.groups()
            if int(contrato_id) == contrato.id and contato_id in contatos_processados:
                try:
                    contato = Contato.objects.get(id=contato_id, contrato=contrato)
                    
                    # Obter ou criar email
                    emails = list(contato.emailcontato_set.all())
                    email_index = int(email_index)
                    
                    if email_index < len(emails):
                        # Atualizar email existente
                        email_obj = emails[email_index]
                        email_obj.email = value
                        email_obj.save()
                    else:
                        # Criar novo email
                        EmailContato.objects.create(contato=contato, email=value)
                        
                except Contato.DoesNotExist:
                    continue
    
    # Processar telefones
    for field_name, value in request.POST.items():
        match = telefone_pattern.match(field_name)
        if match:
            contrato_id, contato_id, telefone_index = match.groups()
            if int(contrato_id) == contrato.id and contato_id in contatos_processados:
                try:
                    contato = Contato.objects.get(id=contato_id, contrato=contrato)
                    
                    # Obter ou criar telefone
                    telefones = list(contato.telefonecontato_set.all())
                    telefone_index = int(telefone_index)
                    
                    if telefone_index < len(telefones):
                        # Atualizar telefone existente
                        telefone_obj = telefones[telefone_index]
                        telefone_obj.telefone = value
                        telefone_obj.save()
                    else:
                        # Criar novo telefone
                        TelefoneContato.objects.create(contato=contato, telefone=value)
                        
                except Contato.DoesNotExist:
                    continue


def _processar_novos_contatos(request, contrato):
    """Processa novos contatos criados via JavaScript"""
    
    # Padrões para identificar campos de novos contatos
    novo_contato_pattern = re.compile(r'novo_contato_nome_(\d+)_(\d+)')
    novo_email_pattern = re.compile(r'novo_email_(\d+)_(\d+)_(\d+)')
    novo_telefone_pattern = re.compile(r'novo_telefone_(\d+)_(\d+)_(\d+)')
    
    # Agrupar dados de novos contatos
    novos_contatos = {}
    
    # Processar nomes de novos contatos
    for field_name, value in request.POST.items():
        match = novo_contato_pattern.match(field_name)
        if match:
            contrato_id, contato_index = match.groups()
            if int(contrato_id) == contrato.id:
                if contato_index not in novos_contatos:
                    novos_contatos[contato_index] = {'nome': '', 'emails': [], 'telefones': []}
                novos_contatos[contato_index]['nome'] = value
    
    # Processar emails de novos contatos
    for field_name, value in request.POST.items():
        match = novo_email_pattern.match(field_name)
        if match:
            contrato_id, contato_index, email_index = match.groups()
            if int(contrato_id) == contrato.id:
                if contato_index not in novos_contatos:
                    novos_contatos[contato_index] = {'nome': '', 'emails': [], 'telefones': []}
                novos_contatos[contato_index]['emails'].append(value)
    
    # Processar telefones de novos contatos
    for field_name, value in request.POST.items():
        match = novo_telefone_pattern.match(field_name)
        if match:
            contrato_id, contato_index, telefone_index = match.groups()
            if int(contrato_id) == contrato.id:
                if contato_index not in novos_contatos:
                    novos_contatos[contato_index] = {'nome': '', 'emails': [], 'telefones': []}
                novos_contatos[contato_index]['telefones'].append(value)
    
    # Criar novos contatos
    for contato_index, dados in novos_contatos.items():
        if dados['nome']:  # Só criar se tiver nome
            novo_contato = Contato.objects.create(
                contrato=contrato,
                nome=dados['nome']
            )
            
            # Criar emails
            for email in dados['emails']:
                if email:  # Só criar se não estiver vazio
                    EmailContato.objects.create(contato=novo_contato, email=email)
            
            # Criar telefones
            for telefone in dados['telefones']:
                if telefone:  # Só criar se não estiver vazio
                    TelefoneContato.objects.create(contato=novo_contato, telefone=telefone)


def _criar_forms_contrato(contrato):
    """Cria formulários para um contrato específico"""
    
    # Obter instâncias relacionadas ou None se não existirem
    try:
        vigencia = contrato.vigencia
    except Vigencia.DoesNotExist:
        vigencia = None
        
    try:
        links = contrato.links
    except Links.DoesNotExist:
        links = None
        
    try:
        garantia = contrato.garantia
    except Garantia.DoesNotExist:
        garantia = None
        
    try:
        gestor = contrato.gestor
    except Gestor.DoesNotExist:
        gestor = None
        
    # Para contatos, pegar o primeiro se existir
    contato = contrato.contato_set.first()
    email_contato = None
    telefone_contato = None
    
    if contato:
        email_contato = contato.emailcontato_set.first()
        telefone_contato = contato.telefonecontato_set.first()
    
    # Criar forms individuais com prefixos únicos
    contrato_form = ContratoForm(instance=contrato, prefix='contrato')
    vigencia_form = VigenciaForm(instance=vigencia, prefix='vigencia')
    links_form = LinksForm(instance=links, prefix='links')
    garantia_form = GarantiaForm(instance=garantia, prefix='garantia')
    gestor_form = GestorForm(instance=gestor, prefix='gestor')
    contato_form = ContatoForm(instance=contato, prefix='contato')
    email_contato_form = EmailContatoForm(instance=email_contato, prefix='email_contato')
    telefone_contato_form = TelefoneContatoForm(instance=telefone_contato, prefix='telefone_contato')
    
    return {
        'contrato_form': contrato_form,
        'vigencia_form': vigencia_form,
        'links_form': links_form,
        'garantia_form': garantia_form,
        'gestor_form': gestor_form,
        'contato_form': contato_form,
        'email_contato_form': email_contato_form,
        'telefone_contato_form': telefone_contato_form,
    }

def profile(request):
    return render(request, "pages/profile.html")


def updateContracts(request):
    search = request.GET.get('search', '')

    contratos_list = Contrato.objects.all().order_by('numero_contrato')
    if search:
        contratos_list = contratos_list.filter(
            Q(entidade__icontains=search) |
            Q(cnpj_cpf__icontains=search) |
            Q(numero_contrato__icontains=search)
        )

    paginator = Paginator(contratos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, "pages/updateContracts.html", context)

def profile(request):
    return render(request, "pages/profile.html")


def updateContracts(request):
    search = request.GET.get('search', '')

    contratos_list = Contrato.objects.all().order_by('numero_contrato')
    if search:
        contratos_list = contratos_list.filter(
            Q(entidade__icontains=search) |
            Q(cnpj_cpf__icontains=search) |
            Q(numero_contrato__icontains=search)
        )

    paginator = Paginator(contratos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, "pages/updateContracts.html", context)