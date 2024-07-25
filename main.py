import os
import time

from models import Config
from models.page import Page
from utils import (
    exit_application,
    get_pdf_docs,
    message,
    page_message,
    set_title,
    success,
    warn,
)

def main():
    try:
        config = Config()

        _input = config.get_input_folder()
        _output =config.get_output_folder()
        _max = max(len(_input), len(_output)) + 27

        print(" Iniciando...\n", "-" * _max)
        set_title("Iniciando...")
        message("Origem:", end="")
        warn(_input)
        message("Destino:", end="")
        warn(_output)
        print("", "-" * _max)

        pdf_docs = get_pdf_docs()

        processed_pages = 0
        total_pages = 0

        for pdf in pdf_docs:
            doc_name = os.path.basename(pdf.path)
            total = len(pdf.pages)
            total_pages += total

            status = f"Processando arquivo {doc_name}..."
            set_title(status)
            warn(status)

            for current_page in pdf.pages:
                page = Page(pdf, current_page, current_page.page_number)
                saved = page.save()

                if saved:
                    processed_pages += 1

                page_message(page.page_number, total, saved)

            pdf.close()

            print("", "-" * _max)

        msg = f"Número de páginas processadas com sucesso: {processed_pages} de {total_pages}"

        set_title("Concluído!")

        if processed_pages == total_pages:
            success(msg)
        else:
            warn(msg)
    except Exception as e:
        exit_application(e)

    exit_application()


if __name__ == "__main__":
    main()
