import os
import re
from typing import List, Tuple

import fitz
import pdfplumber
from pdfminer.pdfpage import PDFPage

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

def message(page_number, total, success) -> str:
    return f"  Página {page_number} de {total}"

class Page(pdfplumber.page.Page):
    def __init__(
        self,
        pdf: pdfplumber.pdf.PDF,
        page_obj: PDFPage,
        page_number: int,
        initial_doctop: pdfplumber.page.T_num = 0,
    ):
        self.pdf = pdf
        self.root_page = self
        self.page_obj = page_obj
        self.page_number = page_number
        self.initial_doctop = initial_doctop
        self.text = page_obj.extract_text()
        self.dirname = os.path.dirname(self.pdf.path)
        self.filename = os.path.basename(self.pdf.path)

    def __enter__(self) -> "Page":
        return self

    def __exit__(self) -> None:
        self.close()

    def save(self) -> bool:
        success = False

        try:
            doc = fitz.open(self.pdf.path)
            output_pdf = fitz.open()
            output_pdf_pg_num = self.page_number - 1
            output_pdf.insert_pdf(doc, from_page=output_pdf_pg_num, to_page=output_pdf_pg_num)
            output_pdf.save(self.__get_unique_name())
            success = True
        except:
            pass
        finally:
            self.page_obj.close()

        return success

    def __extract_currency_values(self, index: int = None) -> List[Tuple[str, str]]:
        """
        Extrai valores monetários do texto fornecido.

        A função procura por símbolos de moeda (R$, $, €, £) seguidos por valores
        com separadores opcionais de vírgula ou ponto.

        Args:
            index (int, opcional): Um índice específico para retornar apenas o valor encontrado nessa posição.
                                    Se não fornecido, todos os valores encontrados são retornados.
                                    O valor padrão é None.

        Returns:
            list of tuples: Uma lista de tuplas onde cada tupla contém um símbolo de moeda e o valor correspondente.
                            Exemplo: [('R$', '1.234,56'), ('$', '2,345.67'), ('€', '300,50'), ('£', '400.00')]

                            Se um índice for fornecido, retorna apenas a tupla nessa posição.
                            Exemplo: ('R$', '1.234,56')
        """
        # Padrão de expressão regular para encontrar valores monetários
        pattern = r"((?:R\$|\$|\€|\£))\s*(\d+(?:[.,]\d{3})*(?:[.,]\d+)?)"

        # Encontrar todas as correspondências no texto e retornar como uma lista de tuplas
        match = re.findall(pattern, self.text)

        return match[index] if index is not None else match

    def __get_recipient_name(self):
        # Padrão de expressão regular para encontrar valores monetários
        pattern = r"Nome do Destinatário:\s*([a-zA-Z\s]+?)\s*(?:-|\n|$)"

        # Encontrar todas as correspondências no texto e retornar como uma lista de tuplas
        match = re.search(pattern, self.text)

        return match.group(1).strip() if match else None

    def __get_unique_name(self):
        extension = "pdf"
        symbol, value = self.__extract_currency_values(0)
        recipient_name = self.__get_recipient_name()
        doc_name = f"{recipient_name} {symbol} {value}" if recipient_name else f"{symbol} {value}"
        output_dir = os.path.join(self.dirname, default_output_dir_name)
        basename = os.path.join(output_dir, doc_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Padrão de regex para corresponder arquivos com sufixos numéricos
        pattern = re.compile(rf"^{re.escape(doc_name)}(_(\d+))?\.{extension}$")

        # Encontra todos os arquivos existentes que correspondem ao padrão
        existing_files = [f for f in os.listdir(output_dir) if pattern.match(f)]

        # Determina o próximo sufixo numérico disponível
        if existing_files:
            highest_num = 0
            for filename in existing_files:
                match = pattern.match(filename)
                if match and match.group(2):
                    num = int(match.group(2))
                    if num > highest_num:
                        highest_num = num
            next_num = highest_num + 1
            filename = f"{basename}_{next_num}.{extension}"
        else:
            filename = f"{basename}.{extension}"

        return filename