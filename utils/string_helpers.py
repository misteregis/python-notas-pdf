import re


def string_list_to_json(words: str, use_even_indices: bool = True, separator: str = ",") -> dict:
    """
    Converte uma string contendo pares de palavras em um dicionário JSON.

    A string é dividida em uma lista de palavras usando o separador fornecido. Em seguida:
    - Remove o último elemento da lista se ele for uma string vazia.
    - Ajusta a lista para garantir que tenha um número par de elementos (removendo o último elemento se necessário).
    - Cria um dicionário onde, dependendo do valor de `use_even_indices`, os elementos de índice par ou ímpar são usados como chaves e os elementos correspondentes são usados como valores.

    Args:
        words (str): A string contendo pares de palavras separadas por um delimitador.
        use_even_indices (bool): Se True, usa índices pares como chaves e índices ímpares como valores. Se False, usa índices ímpares como chaves e índices pares como valores.
        separator (str): O separador usado para dividir a string em uma lista. O padrão é ','.

    Returns:
        dict: Um dicionário com as palavras de índice par ou ímpar como chaves e as palavras correspondentes como valores.

    Example:
        >>> string_list_to_json("key1,value1,key2,value2", use_even_indices=True, separator=',')
        {'key1': 'value1', 'key2': 'value2'}

        >>> string_list_to_json("value1,key1,value2,key2", use_even_indices=False, separator=',')
        {'key1': 'value1', 'key2': 'value2'}

        >>> string_list_to_json("key1|value1|key2|value2", use_even_indices=True, separator='|')
        {'key1': 'value1', 'key2': 'value2'}
    """

    # Divide a string em uma lista usando o separador fornecido
    word_list = words.split(separator)

    # Remove o último elemento se for vazio
    if word_list[-1] == "":
        word_list = word_list[:-1]

    # Ajusta a lista para ter um número par de elementos, se necessário
    if len(word_list) % 2 != 0:
        word_list = word_list[:-1]  # Remove o último elemento se o número total for ímpar

    # Cria o dicionário usando os índices pares ou ímpares como chave e os índices correspondentes como valor
    if use_even_indices:
        dictionary = {word_list[i]: word_list[i + 1] for i in range(0, len(word_list), 2)}
    else:
        dictionary = {word_list[i + 1]: word_list[i] for i in range(0, len(word_list), 2)}

    return dictionary


def replace_words(text, replacements):
    """
    Substitui palavras em um texto dado com base em um dicionário de substituições.

    Args:
        text (str): O texto original a ser modificado.
        replacements (dict): Um dicionário contendo palavras a serem substituídas como chaves e suas substituições correspondentes como valores.

    Returns:
        str: O texto modificado com as palavras substituídas.

    Example:
        >>> replace_words("Eu amo comer pizza", {"pizza": "sushi"})
        'Eu amo comer sushi'
        >>> replace_words("Eu odeio pizza", {"pizza": "sushi", "odeio": "amo"})
        'Eu amo sushi'
    """

    # Cria um padrão que captura palavras e também os separadores ao redor
    pattern = re.compile(
        r"\b("
        + "|".join(re.escape(word.upper()) for word in replacements.keys())
        + r")\b",
        re.IGNORECASE,
    )

    # Substitui as palavras de acordo com o dicionário e mantém o separador original
    replaced_text = pattern.sub(
        lambda match: replacements.get(match.group(0).upper(), ""), text
    )

    # Remove duplicações de separadores (espaços, hífens, etc.) deixados por substituições
    replaced_text = re.sub(r"([^\w\s]|_)\1+|(\s)\2+", r"\1\2", replaced_text)

    # Remove separadores extras do início ou final da string
    replaced_text = re.sub(r"^[^\w\s]+|[^\w\s]+$", "", replaced_text).strip()

    return replaced_text
