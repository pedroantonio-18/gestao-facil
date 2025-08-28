from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from contratos.models import Contrato, Vigencia, Links, Garantia, Gestor, Contato, EmailContato, TelefoneContato
from datetime import timedelta
from .forms import ContratoForm, VigenciaForm, LinksForm, GarantiaForm, GestorForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request):
    numero = request.GET.get('numero', '')
    entidade = request.GET.get('entidade', '')
    documento = request.GET.get('documento', '')

    # Filtro de contratos
    contratos_query = Contrato.objects.all().order_by('numero_contrato')
    if numero:
        contratos_query = contratos_query.filter(numero_contrato__icontains=numero)
    if entidade:
        contratos_query = contratos_query.filter(entidade__icontains=entidade)
    if documento:
        contratos_query = contratos_query.filter(cnpj_cpf__icontains=documento)

    # Paginação
    paginator = Paginator(contratos_query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contratos vencidos e a vencer
    hoje = timezone.now().date()
    limite = hoje + timedelta(days=30)

    contratos_vencidos = Contrato.objects.filter(vigencia__vigencia_atual__lt=hoje).distinct()
    contratos_a_vencer = Contrato.objects.filter(
        vigencia__vigencia_atual__gte=hoje,
        vigencia__vigencia_atual__lte=limite
    ).distinct()

    # POST para atualizar contrato e suas relações não-dinâmicas
    if request.method == 'POST':
        contrato_id = request.POST.get('contrato_id')
        try:
            contrato = Contrato.objects.get(id=contrato_id)
        except Contrato.DoesNotExist:
            return redirect('home')

        # Obter instâncias relacionadas ou None
        vigencia = getattr(contrato, 'vigencia', None)
        links = getattr(contrato, 'links', None)
        garantia = getattr(contrato, 'garantia', None)
        gestor = getattr(contrato, 'gestor', None)

        # Criar forms
        contrato_form = ContratoForm(request.POST, instance=contrato)
        if contrato_form.is_valid():
            contrato_form.save()

        if vigencia:
            vigencia_form = VigenciaForm(request.POST, instance=vigencia)
            if vigencia_form.is_valid():
                vigencia_form.save()

        if links:
            links_form = LinksForm(request.POST, instance=links)
            if links_form.is_valid():
                links_form.save()

        if garantia:
            garantia_form = GarantiaForm(request.POST, instance=garantia)
            if garantia_form.is_valid():
                garantia_form.save()

        if gestor:
            gestor_form = GestorForm(request.POST, instance=gestor)
            if gestor_form.is_valid():
                gestor_form.save()

        return redirect('home')

    # Criar forms individuais apenas para contratos não-dinâmicos
    forms = []
    for contrato in page_obj:
        contrato_form = ContratoForm(instance=contrato)
        vigencia_form = VigenciaForm(instance=getattr(contrato, 'vigencia', None))
        links_form = LinksForm(instance=getattr(contrato, 'links', None))
        garantia_form = GarantiaForm(instance=getattr(contrato, 'garantia', None))
        gestor_form = GestorForm(instance=getattr(contrato, 'gestor', None))

        form_dict = {
            'contrato_form': contrato_form,
            'vigencia_form': vigencia_form,
            'links_form': links_form,
            'garantia_form': garantia_form,
            'gestor_form': gestor_form,
        }
        forms.append((contrato, form_dict))

    context = {
        'page_obj': page_obj,
        'contratos_filtrados': contratos_query if (numero or entidade or documento) else None,
        'numero': numero,
        'entidade': entidade,
        'documento': documento,
        'contratos_vencidos': contratos_vencidos,
        'contratos_a_vencer': contratos_a_vencer,
        'forms': forms,
    }

    return render(request, 'pages/home.html', context)

@csrf_exempt
def saveContact(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})
    
    print("=== DADOS RECEBIDOS ===")
    print("POST:", request.POST.dict())       # transforma em dict normal
    print("LISTA DE EMAILS:", request.POST.getlist('emails[]'))
    print("LISTA DE TELEFONES:", request.POST.getlist('telefones[]'))
    print("=======================")

    contrato_id = request.POST.get('contrato_id')
    contato_id = request.POST.get('contato_id')
    nome = request.POST.get('nome', '').strip()
    emails = request.POST.getlist('emails[]')
    telefones = request.POST.getlist('telefones[]')

    if not contrato_id or not nome:
        return JsonResponse({'success': False, 'error': 'Dados insuficientes'})

    if contato_id and contato_id != 'novo':
        try:
            contato = Contato.objects.get(id=contato_id, contrato_id=contrato_id)
            contato.nome = nome
            contato.save()
        except Contato.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contato não existe'})
    else:
        contato, created = Contato.objects.get_or_create(
            contrato_id=contrato_id,
            nome=nome
        )

    contato.emailcontato_set.all().delete()
    for email in emails:
        if email.strip():
            EmailContato.objects.create(contato=contato, email=email.strip())

    contato.telefonecontato_set.all().delete()
    for telefone in telefones:
        if telefone.strip():
            TelefoneContato.objects.create(contato=contato, telefone=telefone.strip())

    return JsonResponse({'success': True, 'contato_id': contato.id, 'nome': contato.nome})

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