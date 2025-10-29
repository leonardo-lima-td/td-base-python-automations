"""
Testes para utilitários de string
Testa funcionalidade e edge cases
"""
import pytest
from automacoes_python_base_td.utils.string_utils import (
    slugify,
    truncate,
    capitalize_words,
)


class TestSlugify:
    """Testes para função slugify"""
    
    def test_slugify_basic(self):
        """Testa slugify básico"""
        result = slugify("Hello World")
        assert result == "hello-world"
    
    def test_slugify_with_accents(self):
        """Testa slugify com acentos"""
        result = slugify("Olá Mundo")
        assert result == "ola-mundo"
    
    def test_slugify_with_special_chars(self):
        """Testa slugify com caracteres especiais"""
        result = slugify("Hello @#$ World!!!")
        assert result == "hello-world"
    
    def test_slugify_multiple_spaces(self):
        """Testa slugify com múltiplos espaços"""
        result = slugify("Hello    World")
        assert result == "hello-world"
    
    def test_slugify_empty_string(self):
        """Testa slugify com string vazia"""
        result = slugify("")
        assert result == ""


class TestTruncate:
    """Testes para função truncate"""
    
    def test_truncate_short_text(self):
        """Testa truncate com texto menor que o limite"""
        result = truncate("Hello", 10)
        assert result == "Hello"
    
    def test_truncate_long_text(self):
        """Testa truncate com texto maior que o limite"""
        result = truncate("Hello World", 8)
        assert result == "Hello..."
    
    def test_truncate_exact_length(self):
        """Testa truncate com texto do tamanho exato"""
        result = truncate("Hello", 5)
        assert result == "Hello"
    
    def test_truncate_with_custom_suffix(self):
        """Testa truncate com sufixo customizado"""
        result = truncate("Hello World!!!", 10, suffix=" [...]")
        # max_length=10, suffix=" [...]" (6 chars), então 10-6=4 chars do texto + 6 do suffix = 10 total
        assert result == "Hell [...]"
    
    def test_truncate_empty_string(self):
        """Testa truncate com string vazia"""
        result = truncate("", 10)
        assert result == ""


class TestCapitalizeWords:
    """Testes para função capitalize_words"""
    
    def test_capitalize_words_basic(self):
        """Testa capitalização básica"""
        result = capitalize_words("hello world")
        assert result == "Hello World"
    
    def test_capitalize_words_already_capitalized(self):
        """Testa com palavras já capitalizadas"""
        result = capitalize_words("Hello World")
        assert result == "Hello World"
    
    def test_capitalize_words_mixed_case(self):
        """Testa com caso misto"""
        result = capitalize_words("hELLo WoRLD")
        assert result == "Hello World"
    
    def test_capitalize_words_with_numbers(self):
        """Testa com números"""
        result = capitalize_words("hello 123 world")
        assert result == "Hello 123 World"
    
    def test_capitalize_words_empty_string(self):
        """Testa com string vazia"""
        result = capitalize_words("")
        assert result == ""

