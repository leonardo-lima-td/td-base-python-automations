"""
CLI para inicializar projetos com td-base-python-automations

Uso:
    td-init [nome_do_projeto]
    td-init .  # diretório atual
"""
import os
import shutil
from pathlib import Path
import sys


def get_quick_start_dir():
    """Retorna diretório quick_start do pacote"""
    return Path(__file__).parent / "quick_start"


def init_project(args=None):
    """
    Inicializa estrutura de projeto com quick_start
    
    Args:
        args: Lista de argumentos (opcional, usa sys.argv por padrão)
    """
    # Parse argumentos
    if args is None:
        args = sys.argv[1:] if len(sys.argv) > 1 else ['.']
    
    project_name = args[0] if args else '.'
    
    print("=" * 60)
    print("TD Base Python - Inicialização de Projeto")
    print("=" * 60)
    
    # Determinar caminho do projeto
    if project_name == '.':
        project_path = Path.cwd()
        print(f"Usando diretório atual: {project_path}")
    else:
        project_path = Path(project_name)
        if project_path.exists():
            response = input(f"'{project_name}' já existe. Continuar? (s/n): ")
            if response.lower() != 's':
                print("Cancelado pelo usuário")
                sys.exit(0)
        else:
            project_path.mkdir(parents=True)
            print(f"Diretório criado: {project_path}")
    
    # Obter diretório quick_start
    quick_start = get_quick_start_dir()
    
    if not quick_start.exists():
        print(f"Erro: Diretório quick_start não encontrado em {quick_start}")
        sys.exit(1)

    print(f"\nValidando arquivos de configuração...")

    # Configurar .env
    env_path = project_path / ".env"
    
    if not env_path.exists():
        shutil.copy2(quick_start / "env.example", env_path)
        print(f"   • .env (Criado a partir de env.example)")
    else:
        print(f"   • .env (Arquivo existente, não alterado)")

    # Configurar requirements.txt
    requirements_path = project_path / "requirements.txt"
    requirements_append = "\n\n# Pacote base TD\nautomacoes-python-base-td>=0.1.0\n"
    
    if requirements_path.exists():
        # Verificar se já tem o pacote antes de adicionar
        existing_content = requirements_path.read_text()
        if "automacoes-python-base-td" not in existing_content:
            with requirements_path.open('a') as f:
                f.write(requirements_append)
            print(f"   • requirements.txt (Atualizado, adicionado parametro customizados)")
        else:
            print(f"   • requirements.txt (Contém o pacote, não alterado)")
    
    # Configurar .gitignore
    gitignore_path = project_path / ".gitignore"
    gitignore_append = "\n\n# Project folders\nfiles/\ntemp/\n"
    
    if gitignore_path.exists():
        # Verificar se já tem as pastas antes de adicionar
        existing_content = gitignore_path.read_text()
        if "files/" not in existing_content or "temp/" not in existing_content:
            with gitignore_path.open('a') as f:
                f.write(gitignore_append)
            print(f"   • .gitignore (Atualizado, adicionado parametro customizados)")
        else:
            print(f"   • .gitignore (Contém as configurações, não alterado)")

    # Configurar .dockerignore
    dockerignore_path = project_path / ".dockerignore"
    dockerignore_append = "\n\n# Project folders\nfiles/\ntemp/\n"
    
    if dockerignore_path.exists():
        # Verificar se já tem as pastas antes de adicionar
        existing_content = dockerignore_path.read_text()
        if "files/" not in existing_content or "temp/" not in existing_content:
            with dockerignore_path.open('a') as f:
                f.write(dockerignore_append)
            print(f"   • .dockerignore (Atualizado, adicionado parametro customizados)")
        else:
            print(f"   • .dockerignore (Contém as configurações, não alterado)")


    # Configurar requirements.txt e .gitignore
    print(f"\nCopiando arquivos de quick_start...")
    
    # Copiar todos os arquivos e pastas
    copied_files = []
    
    for item in quick_start.iterdir():
        dest = project_path / item.name
        
        if item.is_file():
            if not dest.exists():
                shutil.copy2(item, dest)
                copied_files.append(item.name)
                print(f"   • {item.name} (arquivo)")
        
        elif item.is_dir():
            # Copiar diretório inteiro
            if not dest.exists():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                num_files = len(list(item.rglob('*')))
                copied_files.append(f"{item.name}/")
                print(f"   • {item.name}/ ({num_files} arquivos)")
    
    # Criar diretórios adicionais para desenvolvimento
    print(f"\nCriando estrutura de diretórios...")
    
    dirs_to_create = [
        "logs",      # Logs da aplicação local
        "data",      # Dados da aplicação persistentes
        "files",     # Arquivos persistentes para automação
        "temp",      # Dados temporários para automação
    ]
    
    for dirname in dirs_to_create:
        dir_path = project_path / dirname
        dir_path.mkdir(exist_ok=True)
        # Criar .gitkeep para manter a pasta no git
        (dir_path / ".gitkeep").touch()
    
    # Resumo
    print("\n" + "=" * 60)    
    print(f"Estrutura criada em: {project_path.absolute()}")
    print(f"    ├── 📂 examples/              # Exemplos de uso")
    print(f"    ├── 📂 logs/                  # Logs da aplicação (auto-criado)")
    print(f"    ├── 📂 data/                  # Dados persistentes (auto-criado)")
    print(f"    ├── 📂 files/                 # Arquivos automação (auto-criado)")
    print(f"    └── 📂 temp/                  # Temporários (auto-criado)")
    
    print("\nPróximos passos:")
    steps = []
    if project_name != '.':
        steps.append(f"cd {project_path.absolute()}")
    steps.extend([
        "Copiar env.example para .env e editar com suas configurações",
        "Instalar dependências: pip install -r requirements.txt",
        "Explorar exemplos em: examples/",
        "Os models do pacote já estão disponíveis para importar"
    ])
    
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    print("\nDica: Leia o README.md para começar!")
    print("Documentação completa: PROJECT_STRUCTURE.txt")
    print("=" * 60)


def main():
    """Entry point para o comando td-init"""
    try:
        init_project()
    except KeyboardInterrupt:
        print("Cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

