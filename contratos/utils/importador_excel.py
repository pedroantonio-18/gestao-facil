from contratos.models import Contrato, Vigencia, Garantia, Gestor, Contato, TelefoneContato, EmailContato, Links
import openpyxl
from datetime import datetime
from pathlib import Path
from decimal import Decimal
import re

# Função para separar o nome e telefone da coluna de contato
def separar_contato(contato: str) -> tuple[str | None, str | None, str | None]:
    if not contato:
        return None, None, None
    
    padrao_telefone = re.compile(r'(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}') # Regex que define o padrão de um número de telefone
    padrao_ramal = re.compile(r'ramal[\s, .-]*(\d+)', re.IGNORECASE) # Regex que define o padrão de um número de telefone se estiver com 'ramal'
    
    telefones_limpos = padrao_telefone.findall(contato)
    telefones_com_ramal = padrao_ramal.findall(contato)

    numeros = []
    for tel in telefones_limpos:
        numeros.append(tel.strip())

    for num in telefones_com_ramal:
        numeros.append(f'Ramal-{num.strip()}')

    telefone1 = numeros[0] if len(numeros) > 0 else None
    telefone2 = numeros[1] if len(numeros) > 1 else None

    texto_limpo = padrao_telefone.sub('', contato)
    texto_limpo = padrao_ramal.sub('', texto_limpo)
    texto_limpo = re.sub(r'\d+', '', texto_limpo)

    nome = texto_limpo.strip(' -–—,;.\n\t')

    return nome, telefone1, telefone2

# Função para substituir 'ramal' por um valor válido
def substituir_ramal(gestor: str, telefone: str) -> str:
    if telefone is None:
        return None
    
    gestor_ramal = {
        'SESAP/URC': '(62) 3357',
        'SESAP/LZA': '(61) 2104',
        'SESAP/FORMOSA': '(61) 2192',
        'SESAP/RVD': '(64) 3211',
        'SETMAT': '(62) 3623',
        'SESEG': '(62) 3226',
        'SEENG': '(62) 32262',
        'SEVIT': '(62) 3226',
        'SECAM': '(62) 3226',
        'SELIT': '(62) 3226',
        'NUTEC': '(62) 3226',
        'NUBES': '(62) 3226',
        'NUCOD': '(62) 3623',
        'SEAFI/ANS': '(62) 4015',
        'SEMAP': '(62) 3623',
        'SEDER': '(62) 3226',
        'SEPOL': '(62) 3226',
        'SETPAT': '(62) 3226'
    }

    if telefone.lower().startswith('ramal-'):
        ramal = telefone.split('-')[1]
        telefone_base = gestor_ramal.get(gestor, '')
        if telefone_base:
            return f'{telefone_base}-{ramal}'
        else:
            return f'Ramal-{ramal}'
    else:
        return telefone
    
# Função auxiliar para transformar valor monetário em string para decimal
def str_para_decimal(valor_str: str) -> Decimal:
    valor = valor_str.strip().replace('R$', '').replace(' ', '')
    tem_virgula = ',' in valor
    tem_ponto = '.' in valor
    
    if tem_virgula and tem_ponto:
        ultima_virgula = valor.rfind(',')
        ultima_ponto = valor.rfind('.')
        if ultima_virgula > ultima_ponto:
            valor = valor.replace('.', '').replace(',', '.')
        else:
            valor = valor.replace(',', '')
    elif tem_virgula and not tem_ponto:
        valor = valor.replace(',', '.')
    
    return Decimal(valor)

# Verifica se há garantia, se houver, formata a garantia para valor numérico
def verificar_garantia(tipo_garantia: str, valor_garantia: str) -> tuple[str, float]:
    if (not tipo_garantia or tipo_garantia.strip().lower() in {'n/a', 'não há'}):
        return None, None
    
    if valor_garantia is None or (isinstance(valor_garantia, str) and valor_garantia.strip() == ''):
        return tipo_garantia.lower(), None
    
    if isinstance(valor_garantia, str):
        valor_decimal = str_para_decimal(valor_garantia)
    else:
        valor_decimal = Decimal(valor_garantia)

    return tipo_garantia.lower(), valor_decimal
    

# Função para realizar a importação de dados da planilha para o banco
def importar_contratos(caminho_arquivo):
    wb = openpyxl.load_workbook(caminho_arquivo, data_only=True) # Abre o arquivo XLSX
    arquivo = wb.active # Acessa a aba ativa da planilha (acessa a planilha em si)
    linhas = 0
    inseridos = 0
    ignorados = 0

    # Itera sobre cada linha da planilha (pula o cabeçalho) e retorna os valores
    for i, linha in enumerate(arquivo.iter_rows(min_row=4, values_only=True)):
        try:
            processo_sei = str(linha[0])
            numero_contrato = linha[1]
            inscricao_generica = linha[2]
            entidade = linha[3]
            cnpj_cpf = linha[4]
            vigencia = linha[5]
            data_vigencia = None
            if vigencia is not None:
                if isinstance(vigencia, datetime):
                    data_vigencia = vigencia.date()
                elif isinstance(vigencia, int):  
                    try:
                        data_vigencia = openpyxl.utils.datetime.from_excel(vigencia).date()
                    except Exception as e:
                        print(f'Linha {i + 4}: Erro ao converter número inteiro do Excel para data: {vigencia} ({e})')
                        ignorados += 1
                        continue
                elif isinstance(vigencia, str):
                    try:
                        data_vigencia = datetime.strptime(vigencia, '%d/%m/%Y').date()
                    except ValueError:
                        print(f'Linha {i + 4}: Formato de data inválido: {vigencia}')
                        ignorados += 1
                        continue
                else:
                    print(f'Linha {i + 4}: Tipo de vigência inválido: {type(vigencia)} - {vigencia}')
                    ignorados += 1
                    continue

            try:
                tipo_garantia, valor_garantia = verificar_garantia(
                    tipo_garantia=linha[7],
                    valor_garantia=linha[8]
                )
            except ValueError as e:
                print(f"Erro ao processar garantia na linha {i + 4}: {e}")
                tipo_garantia, valor_garantia = None, None

            gestor = linha[9]
            if gestor is not None:
                gestor = gestor.upper()
            else:
                gestor = ''
            email = linha[10]
            nome, telefone1, telefone2 = separar_contato(linha[11])
            telefone1 = substituir_ramal(gestor, telefone1)
            telefone2 = substituir_ramal(gestor, telefone2)
            observacoes = linha[12]

            # Criação no banco de dados
            contrato = Contrato.objects.create(
                processo_sei=processo_sei,
                numero_contrato=numero_contrato,
                objeto=inscricao_generica,
                entidade=entidade,
                cnpj_cpf=cnpj_cpf,
                observacoes=observacoes,
                valor_atualizado=0
            )

            vigencia = Vigencia.objects.create(
                contrato=contrato,
                vigencia_original=data_vigencia,
                vigencia_atual=data_vigencia,
                vigencia_max=None
            )

            Garantia.objects.create(
                contrato=contrato,
                tipo_garantia=tipo_garantia,
                valor_garantia=valor_garantia
            )

            Gestor.objects.create(
                contrato=contrato,
                nome=gestor,
                email=email
            )

            contato = Contato.objects.create(
                contrato=contrato,
                nome=nome
            )

            if telefone1:
                TelefoneContato.objects.create(contato=contato, telefone=telefone1)
            if telefone2:
                TelefoneContato.objects.create(contato=contato, telefone=telefone2)

            if email:
                EmailContato.objects.create(contato=contato, email=None)

            Links.objects.create(
                contrato=contrato,
                link_planilhas_sei=None,
                link_convencao_coletiva_sei=None
            )

            print(f'Linha {i + 4}: inserida com sucesso.')            
            inseridos += 1
        except Exception as e:
            print(f'Linha {i + 4}: Erro ao importar contrato {e}')
            ignorados += 1

        linhas += 1

    print(f'\n-------------------------\nQuantidade total de linhas: {linhas}\nQuantidade de linhas inseridas com sucesso: {inseridos}\nQuantidade de linhas ignoradas (erro): {ignorados}')
