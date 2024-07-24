import os

import pdfplumber
from colorama import Fore


def get_pdf_docs() -> list[str]:
    """
    Recupera documentos PDF de uma pasta de entrada ou caminho de arquivo especificado.

    Esta função verifica o caminho de entrada especificado na configuração.
    Se o caminho for um arquivo e terminar com '.pdf', ele abre o PDF e o adiciona à lista de documentos PDF.
    Se o caminho for um diretório, ele percorre o diretório e seus subdiretórios (excluindo a pasta de saída)
    para encontrar e abrir todos os arquivos PDF, adicionando-os à lista de documentos PDF.

    Returns:
        list[str]: Uma lista de documentos PDF abertos.

    Raises:
        Exception: Se nenhum documento PDF for encontrado.

    Notes:
        O caminho da pasta de entrada é recuperado da classe Config.
        A função usa `pdfplumber` para abrir arquivos PDF.
        A função usa `os.walk` para percorrer diretórios.
        A função ignora arquivos localizados na pasta de saída especificada na configuração.

    Example:
        >>> pdf_docs = get_pdf_docs()
        >>> print(len(pdf_docs))
        3
    """
    from models.config import Config

    config = Config()
    pdf_docs = list()
    path = config.get_input_folder()

    if os.path.isfile(path) and path.lower().endswith(".pdf"):
        pdf_docs.append(pdfplumber.open(path))
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            if config.get_output_folder() in root:
                continue

            for file in files:
                if file.lower().endswith(".pdf"):
                    file_name = os.path.join(root, file)
                    pdf_docs.append(pdfplumber.open(file_name))

    if pdf_docs:
        return pdf_docs
    else:
        raise Exception(f"{Fore.LIGHTRED_EX}Nenhum documento encontrado!{Fore.RESET}")


__all__ = ["get_pdf_docs"]
