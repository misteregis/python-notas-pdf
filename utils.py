import os

import pdfplumber

from page import Page

default_output_dir_name = "output"

def get_pdf_docs(path: str) -> list[str]:
    """
    Obtém documentos PDF a partir de um caminho fornecido.

    Esta função aceita um caminho que pode ser um arquivo PDF ou um diretório contendo arquivos PDF.
    Se for um arquivo PDF, ele será aberto e adicionado à lista de documentos.
    Se for um diretório, todos os arquivos PDF dentro dele (e seus subdiretórios) serão abertos e adicionados à lista de documentos.

    Args:
        path (str): O caminho para um arquivo PDF ou um diretório contendo arquivos PDF.

    Returns:
        list[str]: Uma lista contendo o caminho dos arquivos PDF encontrados.

    Raises:
        Exception: Se nenhum documento PDF for encontrado no caminho fornecido.
    """
    pdf_docs = list()

    if os.path.isfile(path) and path.lower().endswith(".pdf"):
        pdf_docs.append(pdfplumber.open(path))
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            if default_output_dir_name in root:
                continue

            for file in files:
                if file.lower().endswith(".pdf"):
                    file_name = os.path.join(root, file)
                    pdf_docs.append(pdfplumber.open(file_name))

    if pdf_docs:
        return pdf_docs
    else:
        raise Exception("Nenhum documento encontrado!")

def message(page_number, total) -> str:
    return f"  Página {page_number} de {total}"