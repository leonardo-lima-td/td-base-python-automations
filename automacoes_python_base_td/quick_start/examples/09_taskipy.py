"""
09 - Exemplo de Uso do Taskipy
===============================

Este exemplo demonstra como usar o Taskipy para automatizar tarefas
comuns de desenvolvimento no seu projeto.

Taskipy é um task runner simples e eficiente para Python, definido
no pyproject.toml.
"""

import subprocess
import sys
from pathlib import Path


def executar_comando(comando: str, descricao: str) -> bool:
    """
    Executa um comando e retorna se foi bem-sucedido
    
    Args:
        comando: Comando a ser executado
        descricao: Descrição do que o comando faz
        
    Returns:
        bool: True se bem-sucedido, False caso contrário
    """
    print(f"\n{'='*60}")
    print(f"🔧 {descricao}")
    print(f"{'='*60}")
    print(f"Executando: {comando}\n")
    
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {descricao} - SUCESSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {descricao} - ERRO")
        return False


def main():
    """Demonstra o uso de tarefas do Taskipy"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              EXEMPLO DE USO DO TASKIPY                       ║
║              Automação de Tarefas Python                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

O Taskipy permite definir tarefas no pyproject.toml e executá-las
facilmente com o comando 'task <nome-da-tarefa>'.

TAREFAS DISPONÍVEIS:
────────────────────────────────────────────────────────────────
    """)
    
    tarefas = {
        "format": "Formatar código automaticamente com Ruff",
        "format-check": "Verificar formatação sem modificar",
        "lint": "Executar linter para verificar qualidade do código",
        "test": "Executar testes com pytest",
        "test-cov": "Executar testes com cobertura",
        "clean": "Limpar arquivos temporários (__pycache__, .pyc)",
        "build": "Construir o pacote",
        "install-dev": "Instalar em modo desenvolvimento",
        "all-checks": "Executar format + lint + test",
    }
    
    for tarefa, descricao in tarefas.items():
        print(f"  task {tarefa:<15} - {descricao}")
    
    print("\n" + "="*60)
    print("\n💡 EXEMPLO PRÁTICO\n")
    
    # Verificar se o usuário quer executar exemplos
    print("Vamos demonstrar algumas tarefas comuns:\n")
    
    # 1. Verificar formatação
    print("1️⃣  Verificando formatação do código...")
    print("    Comando: task format-check")
    print("    Equivalente a: ruff format --check .")
    
    # 2. Executar linter
    print("\n2️⃣  Verificando qualidade do código com linter...")
    print("    Comando: task lint")
    print("    Equivalente a: ruff check .")
    
    # 3. Executar testes
    print("\n3️⃣  Executando testes...")
    print("    Comando: task test")
    print("    Equivalente a: pytest -v")
    
    # 4. Executar todas as verificações
    print("\n4️⃣  Executando todas as verificações...")
    print("    Comando: task all-checks")
    print("    Equivalente a: task format && task lint && task test")
    
    print("\n" + "="*60)
    print("\n🎯 CASOS DE USO COMUNS\n")
    
    casos_uso = [
        {
            "titulo": "Antes de Fazer Commit",
            "comando": "task all-checks",
            "descricao": "Garante que o código está formatado, sem erros e testes passando"
        },
        {
            "titulo": "Durante Desenvolvimento",
            "comando": "task format && task lint",
            "descricao": "Formata e verifica o código rapidamente"
        },
        {
            "titulo": "CI/CD Pipeline",
            "comando": "task test-cov",
            "descricao": "Executa testes com cobertura para relatórios"
        },
        {
            "titulo": "Limpeza de Projeto",
            "comando": "task clean",
            "descricao": "Remove arquivos temporários e cache"
        },
        {
            "titulo": "Build de Produção",
            "comando": "task clean && task all-checks && task build",
            "descricao": "Limpa, verifica tudo e constrói o pacote"
        },
    ]
    
    for i, caso in enumerate(casos_uso, 1):
        print(f"{i}. {caso['titulo']}")
        print(f"   $ {caso['comando']}")
        print(f"   → {caso['descricao']}\n")
    
    print("="*60)
    print("\n⚙️  CONFIGURAÇÃO NO pyproject.toml\n")
    
    print("""
As tarefas são definidas na seção [tool.taskipy.tasks]:

[tool.taskipy.tasks]
lint = "ruff check ."
format = "ruff format ."
format-check = "ruff format --check ."
test = "pytest -v"
test-cov = "pytest --cov=automacoes_python_base_td --cov-report=html"
clean = "find . -type d -name '__pycache__' -exec rm -rf {} +"
build = "python -m build"
install-dev = "pip install -e '.[dev]'"
all-checks = "task format && task lint && task test"
    """)
    
    print("\n" + "="*60)
    print("\n🔗 ENCADEAMENTO DE TAREFAS\n")
    
    print("""
Você pode encadear múltiplas tarefas usando && ou criar tarefas compostas:

# Executar tarefas em sequência
task format && task lint && task test

# Ou usar a tarefa composta
task all-checks

# Com poetry
poetry run task all-checks

# Em scripts shell
#!/bin/bash
task clean
task format
task lint
task test
task build
    """)
    
    print("\n" + "="*60)
    print("\n📝 CRIANDO SUAS PRÓPRIAS TAREFAS\n")
    
    print("""
Você pode adicionar suas próprias tarefas no pyproject.toml:

[tool.taskipy.tasks]
# Tarefa customizada
deploy = "task all-checks && ./deploy.sh"

# Tarefa com múltiplos comandos
prepare-release = '''
    task clean
    task all-checks
    task build
    echo "Release preparada!"
'''

# Tarefa com argumentos
run-dev = "python -m uvicorn main:app --reload"

# Tarefa de documentação
docs = "mkdocs serve"
docs-build = "mkdocs build"
    """)
    
    print("\n" + "="*60)
    print("\n🎓 DICAS E BOAS PRÁTICAS\n")
    
    dicas = [
        "Use 'task all-checks' antes de cada commit",
        "Configure hooks do git para executar tarefas automaticamente",
        "Crie tarefas específicas para diferentes ambientes (dev, staging, prod)",
        "Documente suas tarefas customizadas no README do projeto",
        "Use tarefas compostas para fluxos de trabalho complexos",
        "Integre com CI/CD executando 'task test-cov' nos pipelines",
    ]
    
    for i, dica in enumerate(dicas, 1):
        print(f"  {i}. {dica}")
    
    print("\n" + "="*60)
    print("\n🔧 INTEGRAÇÃO COM GIT HOOKS\n")
    
    print("""
Você pode integrar o Taskipy com git hooks usando o pre-commit:

# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: taskipy-checks
        name: Run Taskipy checks
        entry: task all-checks
        language: system
        pass_filenames: false

Ou criar um hook manual:

# .git/hooks/pre-commit
#!/bin/bash
task format
task lint

if [ $? -ne 0 ]; then
    echo "❌ Verificações falharam. Corrija os erros antes de commitar."
    exit 1
fi
    """)
    
    print("\n" + "="*60)
    print("\n✨ EXEMPLO INTERATIVO\n")
    
    resposta = input("Deseja ver a lista de tarefas disponíveis no projeto? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        print("\nExecutando: task --list\n")
        try:
            # Tenta listar as tarefas
            subprocess.run(["task", "--list"], check=False)
        except FileNotFoundError:
            print("⚠️  Taskipy não está instalado.")
            print("    Instale com: pip install -e '.[dev]'")
    
    print("\n" + "="*60)
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  Para começar a usar o Taskipy:                              ║
║                                                              ║
║  1. Instale as dependências de dev:                          ║
║     pip install -e ".[dev]"                                  ║
║                                                              ║
║  2. Execute qualquer tarefa:                                 ║
║     task <nome-da-tarefa>                                    ║
║                                                              ║
║  3. Veja todas as tarefas disponíveis:                       ║
║     task --list                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário.")
        sys.exit(0)

