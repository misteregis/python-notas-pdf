import os
import re
from typing import List, Tuple

import fitz
import pdfplumber
from pdfminer.pdfpage import PDFPage

from models.config import Config
from utils.helper import *
from utils.string_helpers import replace_words

DEFAULT_OUTPUT_DIR_NAME = "output"


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
        self.config = Config()

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
            output_pdf.insert_pdf(
                doc,
                from_page=output_pdf_pg_num,
                to_page=output_pdf_pg_num
            )
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

        A função procura por palavras específicas seguidos por valores
        com separadores opcionais de ponto ou vírgula.

        Args:
            index (int, opcional): Um índice específico para retornar apenas o valor encontrado nessa posição.
                                    Se não fornecido, todos os valores encontrados serão retornados.
                                    O valor padrão é None.

        Returns:
            list of tuples: Uma lista de tuplas onde cada tupla contém a palavra identificada e o valor correspondente.
                            Exemplo: [('Valor principal', '1.234,56'), ('Valor nominal', '2,345.67'), ('Valor total', '300,50'), ('Valor', '400.00')]

                            Se um índice for fornecido, retorna apenas a tupla nessa posição.
                            Exemplo: ('Valor principal', '1.234,56')
        """

        words = "|".join(self.config.get_key_values())
        pattern_symbol = rf"({words}):?\s*R?\$?\s?"
        pattern_value = r"(\d+(?:[.,]\d{3})*(?:[.,]\d+)?)"
        pattern = pattern_symbol + pattern_value

        # Encontra todas as correspondências no texto e retorna como uma lista de tuplas
        match = re.findall(pattern, self.text, re.IGNORECASE)

        return match[index] if index is not None else match

    def __get_bank_acronym(self) -> str | None:
        bank_acronyms = self.config.get_bank_acronyms()

        for bank_name, bank_acronym in bank_acronyms.items():
            if bank_name in self.text.upper():
                return bank_acronym

        return None

    def __get_recipient_name(self):
        words = "|".join(["NOME DO DESTINATÁRIO", "FAVORECIDO"])

        # Padrão de expressão regular para encontrar textos após as palavras específicas
        pattern = rf"({words}):?\s*([a-zA-Z\s]+?)\s*(?:-|\n|$)"

        match = re.search(pattern, self.text, re.IGNORECASE)

        return match.group(2).strip() if match else None

    def __get_unique_name(self):
        extension = "pdf"
        _, value = self.__extract_currency_values(0)
        recipient_name = self.__get_recipient_name()
        bank_acronym = self.__get_bank_acronym()
        words = {
            "BANK": bank_acronym,
            "RECIPIENT": recipient_name,
            "VALUE": value
        }

        doc_name = replace_words(self.config.get_output_filename(), words)

        output_dir = self.config.get_output_folder()
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
