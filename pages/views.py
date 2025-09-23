from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from contratos.models import Contrato, Vigencia, Links, Garantia, Gestor, Contato, EmailContato, TelefoneContato
from datetime import timedelta
from .forms import ContratoForm, VigenciaForm, LinksForm, GarantiaForm, GestorForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def home(request ):
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
    print("POST:", request.POST.dict())
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
    if request.method == "POST":
        contrato_id = request.POST.get("contrato_id")
        responsaveis_json = request.POST.get("responsaveis_json")

        if not contrato_id:
            messages.error(request, "Erro: Nenhum contrato foi selecionado para atualização.")
            return redirect("update_contracts")

        contrato_obj = get_object_or_404(Contrato, pk=contrato_id)
        
        vigencia_obj = getattr(contrato_obj, "vigencia", None)
        links_obj = getattr(contrato_obj, "links", None)
        garantia_obj = getattr(contrato_obj, "garantia", None)
        gestor_obj = getattr(contrato_obj, "gestor", None)

        contrato_form = ContratoForm(request.POST, instance=contrato_obj)
        vigencia_form = VigenciaForm(request.POST, instance=vigencia_obj)
        links_form = LinksForm(request.POST, instance=links_obj)
        garantia_form = GarantiaForm(request.POST, instance=garantia_obj)
        gestor_form = GestorForm(request.POST, instance=gestor_obj)

        forms_sao_validos = all([
            contrato_form.is_valid(), 
            vigencia_form.is_valid(), 
            links_form.is_valid(), 
            garantia_form.is_valid(), 
            gestor_form.is_valid()
        ])

        if forms_sao_validos:
            contrato_form.save()
            vigencia = vigencia_form.save(commit=False)
            vigencia.contrato = contrato_obj
            vigencia.save()
            links = links_form.save(commit=False)
            links.contrato = contrato_obj
            links.save()
            garantia = garantia_form.save(commit=False)
            garantia.contrato = contrato_obj
            garantia.save()
            gestor = gestor_form.save(commit=False)
            gestor.contrato = contrato_obj
            gestor.save()

            try:
                responsaveis_data = json.loads(responsaveis_json)
                contrato_obj.contato_set.all().delete()
                for resp_data in responsaveis_data:
                    novo_contato = Contato.objects.create(
                        contrato=contrato_obj,
                        nome=resp_data.get("nome", "Sem nome")
                    )
                    for email_str in resp_data.get("emails", []):
                        if email_str:
                            EmailContato.objects.create(contato=novo_contato, email=email_str)
                    for tel_str in resp_data.get("telefones", []):
                        if tel_str:
                            TelefoneContato.objects.create(contato=novo_contato, telefone=tel_str)
            except (json.JSONDecodeError, TypeError):
                messages.warning(request, "Dados dos responsáveis não puderam ser processados.")

            messages.success(request, f"Contrato \"{contrato_obj.numero_contrato}\" atualizado com sucesso!")
        else:
            messages.error(request, "Não foi possível salvar. Verifique os dados do contrato.")
            print("\n--- INÍCIO DOS ERROS DE VALIDAÇÃO ---")
            if not contrato_form.is_valid(): print("Erros no ContratoForm:", contrato_form.errors.as_json())
            if not vigencia_form.is_valid(): print("Erros no VigenciaForm:", vigencia_form.errors.as_json())
            if not links_form.is_valid(): print("Erros no LinksForm:", links_form.errors.as_json())
            if not garantia_form.is_valid(): print("Erros no GarantiaForm:", garantia_form.errors.as_json())
            if not gestor_form.is_valid(): print("Erros no GestorForm:", gestor_form.errors.as_json())
            print("--- FIM DOS ERROS DE VALIDAÇÃO ---\n")

        return redirect("update_contracts")

    # --- LÓGICA GET (COM A CORREÇÃO) ---
    
    # Bloco de código para buscar notificações (copiado da view 'home')
    hoje = timezone.now().date()
    limite_vencimento = hoje + timedelta(days=30)
    contratos_vencidos = Contrato.objects.filter(vigencia__vigencia_atual__lt=hoje).distinct()
    contratos_a_vencer = Contrato.objects.filter(
        vigencia__vigencia_atual__gte=hoje,
        vigencia__vigencia_atual__lte=limite_vencimento
    ).distinct()

    # Lógica de busca e paginação
    search = request.GET.get("search", "")
    contratos_list = Contrato.objects.all().order_by("numero_contrato")
    if search:
        contratos_list = contratos_list.filter(
            Q(entidade__icontains=search) |
            Q(cnpj_cpf__icontains=search) |
            Q(numero_contrato__icontains=search)
        )
    paginator = Paginator(contratos_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Contexto atualizado para incluir os dados das notificações
    context = {
        "page_obj": page_obj,
        "search": search,
        "contratos_vencidos": contratos_vencidos,
        "contratos_a_vencer": contratos_a_vencer,
    }
    return render(request, "pages/updateContracts.html", context)


def contract(request):
    # Se a requisição for POST, processa os dados do formulário
    if request.method == 'POST':
        # Instancia cada formulário com os dados recebidos
        contrato_form = ContratoForm(request.POST)
        vigencia_form = VigenciaForm(request.POST)
        links_form = LinksForm(request.POST)
        garantia_form = GarantiaForm(request.POST)
        gestor_form = GestorForm(request.POST)

        # Coleta dados que não estão nos forms (contato)
        nome_contato = request.POST.get('nome_contato')
        email_contato = request.POST.get('email_contato')
        telefone_contato = request.POST.get('telefone_contato')
        
        # Lista de todos os forms para validação
        forms_a_validar = [contrato_form, vigencia_form, links_form, garantia_form, gestor_form]

        # Verifica se TODOS os formulários são válidos
        if all(form.is_valid() for form in forms_a_validar):
            try:
                # --- Lógica de salvamento em duas etapas ---
                
                # 1. Salva o Contrato principal, mas sem commit no banco ainda
                novo_contrato = contrato_form.save(commit=False)
                
                # Gera e atribui o número do contrato e o processo SEI
                novo_contrato.numero_contrato = Contrato().gerar_numero_contrato
                novo_contrato.processo_sei = request.POST.get('processo_sei') # Pega o processo SEI
                
                # Agora salva o contrato principal no banco
                novo_contrato.save()

                # 2. Salva os outros objetos, associando-os ao contrato recém-criado
                vigencia = vigencia_form.save(commit=False)
                vigencia.contrato = novo_contrato
                vigencia.vigencia_atual = vigencia.vigencia_original # Define vigencia_atual
                vigencia.save()

                links = links_form.save(commit=False)
                links.contrato = novo_contrato
                links.save()

                garantia = garantia_form.save(commit=False)
                garantia.contrato = novo_contrato
                garantia.save()

                gestor = gestor_form.save(commit=False)
                gestor.contrato = novo_contrato
                gestor.save()

                # Salva o Contato (Responsável) se o nome foi fornecido
                if nome_contato:
                    contato_obj = Contato.objects.create(contrato=novo_contrato, nome=nome_contato)
                    if email_contato:
                        EmailContato.objects.create(contato=contato_obj, email=email_contato)
                    if telefone_contato:
                        TelefoneContato.objects.create(contato=contato_obj, telefone=telefone_contato)

                # Adiciona a mensagem de sucesso para a confirmação visual
                messages.success(request, f'Contrato "{novo_contrato.numero_contrato}" foi registrado com sucesso!')
                return redirect('home')

            except Exception as e:
                messages.error(request, f'Ocorreu um erro inesperado ao salvar: {e}')
        
        else:
            # Se algum formulário for inválido
            messages.error(request, 'Não foi possível salvar. Por favor, corrija os erros abaixo.')
            # A view continuará para renderizar a página com os erros

    # Se a requisição for GET, cria instâncias de formulários em branco
    else:
        contrato_form = ContratoForm()
        vigencia_form = VigenciaForm()
        links_form = LinksForm()
        garantia_form = GarantiaForm()
        gestor_form = GestorForm()

    # Junta todos os formulários em um dicionário para enviar ao template
    context = {
        'contrato_form': contrato_form,
        'vigencia_form': vigencia_form,
        'links_form': links_form,
        'garantia_form': garantia_form,
        'gestor_form': gestor_form,
    }
    
    return render(request, 'pages/contract.html', context)

