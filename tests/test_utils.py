"""
Testes para módulo utils
"""
import pytest
import os
import tempfile
from automacoes_python_base_td.utils import (
    listdir, exists, getsize, isfile, isdir,
    create_dir, write_file, read_file,
    slugify, truncate, capitalize_words,
    format_timestamp, parse_date,
)


class TestFileUtils:
    """Testes para file_utils"""
    
    def test_create_and_write_file(self):
        """Testa criação e escrita de arquivo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.txt")
            
            # Escrever
            assert write_file(filepath, "Hello World!")
            
            # Verificar existência
            assert exists(filepath)
            assert isfile(filepath)
            
            # Ler
            content = read_file(filepath)
            assert content == "Hello World!"
            
            # Verificar tamanho
            assert getsize(filepath) > 0
    
    def test_create_dir(self):
        """Testa criação de diretório"""
        with tempfile.TemporaryDirectory() as tmpdir:
            newdir = os.path.join(tmpdir, "testdir")
            
            assert create_dir(newdir)
            assert exists(newdir)
            assert isdir(newdir)
    
    def test_listdir(self):
        """Testa listagem de arquivos"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Criar alguns arquivos
            write_file(os.path.join(tmpdir, "file1.txt"), "test")
            write_file(os.path.join(tmpdir, "file2.csv"), "test")
            write_file(os.path.join(tmpdir, "file3.txt"), "test")
            
            # Listar todos
            files = listdir(tmpdir)
            assert len(files) == 3
            
            # Listar com filtro
            txt_files = listdir(tmpdir, filter_ext=".txt")
            assert len(txt_files) == 2


class TestStringUtils:
    """Testes para string_utils"""
    
    def test_slugify(self):
        """Testa slugify"""
        assert slugify("Hello World!") == "hello-world"
        assert slugify("Test 123") == "test-123"
        assert slugify("Olá Mundo!") == "ol-mundo"
    
    def test_truncate(self):
        """Testa truncate"""
        text = "Este é um texto longo"
        truncated = truncate(text, 10)
        assert len(truncated) == 10
        assert truncated.endswith("...")
    
    def test_capitalize_words(self):
        """Testa capitalize_words"""
        assert capitalize_words("hello world") == "Hello World"
        assert capitalize_words("python is great") == "Python Is Great"


class TestDateUtils:
    """Testes para date_utils"""
    
    def test_format_timestamp(self):
        """Testa format_timestamp"""
        from datetime import datetime
        
        dt = datetime(2025, 10, 28, 14, 30, 0)
        formatted = format_timestamp(dt)
        assert "2025-10-28" in formatted
        assert "14:30:00" in formatted
    
    def test_parse_date(self):
        """Testa parse_date"""
        date = parse_date("2025-10-28")
        assert date is not None
        assert date.year == 2025
        assert date.month == 10
        assert date.day == 28

