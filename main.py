import os

from utils import Page, get_pdf_docs, message


def main():
    try:
        pdf_docs = get_pdf_docs("notas")

        processed_pages = 0
        total_pages = 0

        for pdf in pdf_docs:
            doc_name = os.path.basename(pdf.path)
            total = len(pdf.pages)
            total_pages += total

            print(f"Processando arquivo {doc_name}...")

            for current_page in pdf.pages:
                page = Page(pdf, current_page, current_page.page_number)
                success = page.save()

                if success:
                    processed_pages += 1

                print(message(page.page_number, total))

            pdf.close()

            print("-" * 50)

        print(f"Número de páginas processas com sucesso: {processed_pages} de {total_pages}\n\t")
    except Exception as e:
        print(e)

    os.system("pause")

if __name__ == "__main__":
    main()