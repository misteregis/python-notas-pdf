# Projeto: Processamento de Notas em PDF

## Descrição

Este projeto é uma aplicação Python para processar documentos PDF e extrair informações de cada página. Ele utiliza bibliotecas como `pdfplumber` e `pdfminer` para manipulação e extração de dados dos PDFs.

## Estrutura do Projeto

- **main.py**: Ponto de entrada da aplicação.
- **requirements.txt**: Lista de dependências do projeto.
- **singleton.py**: Implementação do padrão Singleton.
- **models/**:
  - **config.py**: Configurações do projeto.
  - **config_manager.py**: Gerenciamento de configurações.
  - **page.py**: Classe [Page](models/page.py#L15) para processamento de páginas PDF.
  - **__init__.py**: Inicializador do pacote `models`.
- **utils/**:
  - **constants.py**: Constantes utilizadas no projeto.
  - **file_helpers.py**: Funções auxiliares para seleção de pastas e manipulação de arquivos.
  - **helper.py**: Funções auxiliares diversas.
  - **message.py**: Funções para exibição de mensagens.
  - **string_helpers.py**: Funções auxiliares para manipulação de strings.
  - **__init__.py**: Inicializador do pacote `utils`.

## Uso

1. **Instalação das Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Execução da Aplicação**:
    ```bash
    python main.py
    ```

## Funcionalidades

- **Processamento de PDF**: A aplicação percorre todos os documentos PDF e processa cada página.
- **Extração de Texto**: Utiliza `pdfplumber` para extrair texto das páginas.
- **Mensagens de Status**: Exibe mensagens de progresso e sucesso durante o processamento.

## Dependências

- `pdfplumber`
- `pdfminer.six`
- `PyMuPDF`

## Estrutura de Código

### main.py

O arquivo `main.py` inicializa a aplicação, obtém os documentos PDF a serem processados e usa a classe [Page](models/page.py#L15) para processar cada página.

### models/page.py

A classe [Page](models/page.py#L15) é responsável por manipular e processar as páginas dos PDFs, extraindo texto e salvando as informações necessárias.

### utils/helper.py

Contém funções auxiliares para operações como configuração de título ([set_title](utils/helper.py#L7)).