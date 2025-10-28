"""
Utilitários para manipulação de strings
"""
import re
import unicodedata


def slugify(text: str) -> str:
    """
    Converte uma string para slug (URL-friendly).
    
    Args:
        text: Texto a converter
    
    Returns:
        String no formato slug
    
    Exemplo:
        slug = slugify("Hello World! 123")  # "hello-world-123"
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Trunca uma string para um tamanho máximo.
    
    Args:
        text: Texto a truncar
        max_length: Tamanho máximo
        suffix: Sufixo a adicionar (default: "...")
    
    Returns:
        String truncada
    
    Exemplo:
        truncated = truncate("Hello World!", 8)  # "Hello..."
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def capitalize_words(text: str) -> str:
    """
    Capitaliza cada palavra de uma string.
    
    Args:
        text: Texto a capitalizar
    
    Returns:
        String com palavras capitalizadas
    
    Exemplo:
        capitalized = capitalize_words("hello world")  # "Hello World"
    """
    return ' '.join(word.capitalize() for word in text.split())


def remover_acentos(txt: str) -> str:
    """
    Remove acentos de uma string.
    
    Args:
        txt: Texto a remover acentos
    
    Returns:
        String sem acentos
    """
    nfkd = unicodedata.normalize("NFD", txt)
    return re.sub(r"[\u0300-\u036f]|[\u00a0-\u00e7]|[\u00e3]", "", nfkd)