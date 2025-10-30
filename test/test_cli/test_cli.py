"""
Testes para o CLI de inicialização de projetos
"""
import pytest
from pathlib import Path
import shutil
import tempfile
from automacoes_python_base_td.cli import init_project, get_quick_start_dir


class TestCLI:
    """Testes para o comando td-init"""

    def test_get_quick_start_dir(self):
        """Testa se o diretório quick_start é encontrado"""
        quick_start = get_quick_start_dir()
        assert quick_start.exists()
        assert quick_start.is_dir()
        assert (quick_start / "README.md").exists()
        assert (quick_start / "env.example").exists()
        assert (quick_start / "examples").is_dir()

    def test_init_project_in_temp_dir(self, monkeypatch, tmp_path):
        """Testa inicialização de projeto em diretório temporário"""
        project_name = "test_project"
        project_path = tmp_path / project_name

        # Simular argumentos
        monkeypatch.setattr('sys.argv', ['td-init', str(project_path)])

        # Executar init_project
        init_project([str(project_path)])

        # Verificar se diretório foi criado
        assert project_path.exists()
        assert project_path.is_dir()

        # Verificar arquivos copiados de quick_start
        assert (project_path / "README.md").exists()
        assert (project_path / "env.example").exists()
        assert (project_path / "LICENSE").exists()
        assert (project_path / "PROJECT_STRUCTURE.txt").exists()
        assert (project_path / "examples").is_dir()

        # Verificar arquivos gerados (NÃO deve criar .env)
        assert not (project_path / ".env").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / ".gitignore").exists()

        # Verificar diretórios criados
        assert (project_path / "logs").is_dir()
        assert (project_path / "data").is_dir()
        assert (project_path / "files").is_dir()
        assert (project_path / "temp").is_dir()

        # Verificar .gitkeep
        assert (project_path / "logs" / ".gitkeep").exists()
        assert (project_path / "data" / ".gitkeep").exists()
        assert (project_path / "files" / ".gitkeep").exists()
        assert (project_path / "temp" / ".gitkeep").exists()

        # Verificar que models/ NÃO foi criado
        assert not (project_path / "models").exists()

    def test_init_project_current_dir(self, monkeypatch, tmp_path):
        """Testa inicialização no diretório atual"""
        # Mudar para diretório temporário
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Executar init_project com '.'
            init_project(['.'])

            # Verificar arquivos no diretório atual (NÃO deve criar .env)
            assert (tmp_path / "README.md").exists()
            assert not (tmp_path / ".env").exists()
            assert (tmp_path / "requirements.txt").exists()
            assert (tmp_path / "logs").is_dir()
            assert (tmp_path / "files").is_dir()
            assert (tmp_path / "temp").is_dir()

        finally:
            os.chdir(old_cwd)

    def test_requirements_content(self, tmp_path):
        """Testa conteúdo do requirements.txt gerado"""
        project_path = tmp_path / "test_req"
        init_project([str(project_path)])

        requirements_file = project_path / "requirements.txt"
        content = requirements_file.read_text()

        assert "automacoes-python-base-td" in content
        assert ">=0.1.0" in content

    def test_gitignore_content(self, tmp_path):
        """Testa conteúdo do .gitignore gerado"""
        project_path = tmp_path / "test_git"
        init_project([str(project_path)])

        gitignore_file = project_path / ".gitignore"
        content = gitignore_file.read_text()

        # Verificar entradas importantes do quick_start/.gitignore
        assert ".env" in content
        assert "*.log" in content
        assert "__pycache__/" in content
        assert "venv/" in content
        assert "logs/" in content
        assert "files/" in content
        assert "temp/" in content

    def test_env_not_created(self, tmp_path):
        """Testa que .env NÃO é criado automaticamente"""
        project_path = tmp_path / "test_env"
        init_project([str(project_path)])

        env_file = project_path / ".env"
        env_example = project_path / "env.example"

        # env.example deve existir, mas .env NÃO
        assert env_example.exists()
        assert not env_file.exists()

    def test_requirements_append_existing(self, tmp_path, monkeypatch):
        """Testa append em requirements.txt existente"""
        project_path = tmp_path / "test_req_append"
        project_path.mkdir()

        # Criar requirements.txt existente
        req_file = project_path / "requirements.txt"
        req_file.write_text("pandas>=2.0.0\nrequests>=2.31.0\n")

        # Mockar input para responder 's' (sim) automaticamente
        monkeypatch.setattr('builtins.input', lambda _: 's')

        # Executar init_project
        init_project([str(project_path)])

        # Verificar que o pacote foi adicionado
        content = req_file.read_text()
        assert "pandas>=2.0.0" in content  # Conteúdo original
        assert "requests>=2.31.0" in content  # Conteúdo original
        assert "automacoes-python-base-td>=0.1.0" in content  # Novo

    def test_gitignore_append_existing(self, tmp_path, monkeypatch):
        """Testa append em .gitignore existente"""
        project_path = tmp_path / "test_git_append"
        project_path.mkdir()

        # Criar .gitignore existente
        git_file = project_path / ".gitignore"
        git_file.write_text("*.pyc\n__pycache__/\n")

        # Mockar input para responder 's' (sim) automaticamente
        monkeypatch.setattr('builtins.input', lambda _: 's')

        # Executar init_project
        init_project([str(project_path)])

        # Verificar que as pastas foram adicionadas
        content = git_file.read_text()
        assert "*.pyc" in content  # Conteúdo original
        assert "__pycache__/" in content  # Conteúdo original
        assert "files/" in content  # Novo
        assert "temp/" in content  # Novo

    def test_examples_directory_copied(self, tmp_path):
        """Testa se diretório examples foi copiado completamente"""
        project_path = tmp_path / "test_examples"
        init_project([str(project_path)])

        examples_dir = project_path / "examples"
        assert examples_dir.exists()
        assert examples_dir.is_dir()

        # Verificar arquivos de exemplo
        expected_files = [
            "01_basic_usage.py",
            "02_database_basic.py",
            "03_database_sqlalchemy.py",
            "04_aws_s3.py",
            "05_rabbitmq.py",
            "06_logger.py",
            "07_utils.py",
            "08_exceptions.py",
            "README.md"
        ]

        for filename in expected_files:
            assert (examples_dir / filename).exists(), f"{filename} não encontrado"

    def test_models_dir_not_created(self, tmp_path):
        """Testa que models/ NÃO é criado (já vem no pacote)"""
        project_path = tmp_path / "test_no_models"
        init_project([str(project_path)])

        # models/ não deve existir
        assert not (project_path / "models").exists()

    def test_project_structure_integrity(self, tmp_path):
        """Testa integridade completa da estrutura criada"""
        project_path = tmp_path / "test_full"
        init_project([str(project_path)])

        # Arquivos obrigatórios (NÃO inclui .env - usuário deve criar)
        required_files = [
            "README.md",
            "env.example",
            "LICENSE",
            "PROJECT_STRUCTURE.txt",
            "requirements.txt",
            ".gitignore",
        ]

        for filename in required_files:
            assert (project_path / filename).exists(), f"{filename} obrigatório não encontrado"

        # Diretórios obrigatórios
        required_dirs = [
            "examples",
            "logs",
            "data",
            "files",
            "temp",
        ]

        for dirname in required_dirs:
            assert (project_path / dirname).is_dir(), f"{dirname}/ obrigatório não encontrado"

        # Arquivos que NÃO devem existir
        forbidden_items = [
            "models",  # Não deve criar models/
        ]

        for item in forbidden_items:
            assert not (project_path / item).exists(), f"{item} não deveria existir"

