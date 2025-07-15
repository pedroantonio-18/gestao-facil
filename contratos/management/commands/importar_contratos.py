from django.core.management.base import BaseCommand
from contratos.utils.importador_excel import importar_contratos
from pathlib import Path

class Command(BaseCommand):
    help = 'Importa os contratos a partir da planilha Excel em /excel/Planilha_Contratos.xlsx'

    def handle(self, *args, **kwargs):
        caminho_base = Path.cwd().parent
        caminho_arquivo = caminho_base / 'excel' / 'Planilha_Contratos.xlsx'

        print(f"Caminho do arquivo: {caminho_arquivo}")
        if not caminho_arquivo.exists():
            print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        else:
            importar_contratos(caminho_arquivo)
            print("Importação concluída com sucesso.")