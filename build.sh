#!/bin/bash

# =============================================================================
# Script de Build do Pacote automacoes-python-base-td
# =============================================================================

set -e  # Para no primeiro erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_header() {
    echo -e "\n${BLUE}=========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

print_header "🏗️  BUILD AUTOMACOES-PYTHON-BASE-TD"

# =============================================================================
# 1. LIMPEZA
# =============================================================================
clean() {
    print_header "🧹 Limpando arquivos antigos..."
    
    # Remove builds anteriores
    rm -rf build/ dist/ *.egg-info .eggs/
    print_success "Removido: build/, dist/, *.egg-info"
    
    # Remove cache Python
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    print_success "Removido: __pycache__, *.pyc, *.pyo"
    
    # Remove coverage
    rm -rf htmlcov/ .coverage .pytest_cache/
    print_success "Removido: htmlcov/, .coverage, .pytest_cache/"
    
    print_success "Limpeza concluída!"
}

# =============================================================================
# 2. VERIFICAÇÃO DE DEPENDÊNCIAS
# =============================================================================
check_dependencies() {
    print_header "🔍 Verificando dependências..."
    
    # Verifica Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não encontrado!"
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version)
    print_success "Python: $PYTHON_VERSION"
    
    # Verifica pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 não encontrado!"
        exit 1
    fi
    print_success "pip: $(pip3 --version | cut -d' ' -f2)"
    
    # Verifica build
    if ! python3 -c "import build" 2>/dev/null; then
        print_warning "Módulo 'build' não encontrado. Instalando..."
        pip3 install build
    fi
    print_success "Módulo 'build' instalado"
    
    # Verifica wheel
    if ! python3 -c "import wheel" 2>/dev/null; then
        print_warning "Módulo 'wheel' não encontrado. Instalando..."
        pip3 install wheel
    fi
    print_success "Módulo 'wheel' instalado"
    
    # Verifica twine (opcional, para upload)
    if ! python3 -c "import twine" 2>/dev/null; then
        print_info "Módulo 'twine' não instalado (necessário apenas para upload ao PyPI)"
    else
        print_success "Módulo 'twine' instalado"
    fi
}

# =============================================================================
# 3. VALIDAÇÃO DO CÓDIGO
# =============================================================================
validate() {
    print_header "✨ Validando código..."
    
    # Verifica sintaxe de todos os arquivos Python
    print_info "Verificando sintaxe..."
    if ! python3 -m py_compile automacoes_python_base_td/**/*.py 2>/dev/null; then
        print_error "Erros de sintaxe encontrados!"
        python3 << 'EOF'
import py_compile
import glob
errors = []
for file in glob.glob('automacoes_python_base_td/**/*.py', recursive=True):
    try:
        py_compile.compile(file, doraise=True)
    except Exception as e:
        errors.append(f"{file}: {e}")
        print(f"❌ {file}: {e}")
if errors:
    exit(1)
EOF
        exit 1
    fi
    print_success "Sintaxe OK"
    
    # Verifica pyproject.toml
    if [ ! -f "pyproject.toml" ]; then
        print_error "pyproject.toml não encontrado!"
        exit 1
    fi
    print_success "pyproject.toml encontrado"
    
    # Verifica __init__.py principal
    if [ ! -f "automacoes_python_base_td/__init__.py" ]; then
        print_error "automacoes_python_base_td/__init__.py não encontrado!"
        exit 1
    fi
    print_success "__init__.py principal encontrado"
    
    print_success "Validação concluída!"
}

# =============================================================================
# 4. TESTES (OPCIONAL)
# =============================================================================
run_tests() {
    print_header "🧪 Executando testes..."
    
    if [ ! -d "tests" ]; then
        print_warning "Diretório tests/ não encontrado. Pulando testes."
        return 0
    fi
    
    # Verifica pytest
    if ! command -v pytest &> /dev/null; then
        print_warning "pytest não instalado. Instalando..."
        pip3 install pytest pytest-cov
    fi
    
    # Roda testes
    print_info "Rodando pytest..."
    if pytest tests/ -v --tb=short; then
        print_success "Todos os testes passaram!"
    else
        print_error "Alguns testes falharam!"
        read -p "Continuar com o build? (s/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            exit 1
        fi
    fi
}

# =============================================================================
# 5. BUILD DO PACOTE
# =============================================================================
build_package() {
    print_header "📦 Construindo pacote..."
    
    # Build usando python -m build
    print_info "Executando: python3 -m build"
    if python3 -m build; then
        print_success "Pacote construído com sucesso!"
    else
        print_error "Falha ao construir pacote!"
        exit 1
    fi
    
    # Lista arquivos gerados
    print_info "Arquivos gerados:"
    ls -lh dist/
    
    # Informações sobre os arquivos
    if [ -d "dist" ]; then
        WHL_FILE=$(ls dist/*.whl 2>/dev/null | head -1)
        TAR_FILE=$(ls dist/*.tar.gz 2>/dev/null | head -1)
        
        if [ -n "$WHL_FILE" ]; then
            WHL_SIZE=$(du -h "$WHL_FILE" | cut -f1)
            print_success "Wheel: $(basename $WHL_FILE) ($WHL_SIZE)"
        fi
        
        if [ -n "$TAR_FILE" ]; then
            TAR_SIZE=$(du -h "$TAR_FILE" | cut -f1)
            print_success "Source: $(basename $TAR_FILE) ($TAR_SIZE)"
        fi
    fi
}

# =============================================================================
# 6. VALIDAÇÃO DO PACOTE
# =============================================================================
validate_package() {
    print_header "🔍 Validando pacote..."
    
    # Verifica se twine está instalado
    if ! python3 -c "import twine" 2>/dev/null; then
        print_warning "twine não instalado. Pulando validação."
        return 0
    fi
    
    print_info "Executando: twine check dist/*"
    if twine check dist/*; then
        print_success "Pacote válido!"
    else
        print_error "Pacote inválido!"
        exit 1
    fi
}

# =============================================================================
# 7. INSTALAÇÃO LOCAL (OPCIONAL)
# =============================================================================
install_local() {
    print_header "💻 Instalando localmente..."
    
    print_info "Instalando em modo desenvolvimento..."
    if pip3 install -e .; then
        print_success "Pacote instalado localmente!"
        
        # Testa import
        print_info "Testando import..."
        if python3 -c "import automacoes_python_base_td; print(f'Versão: {automacoes_python_base_td.__version__}')"; then
            print_success "Import funcionando!"
        else
            print_error "Erro ao importar pacote!"
            exit 1
        fi
    else
        print_error "Falha ao instalar pacote!"
        exit 1
    fi
}

# =============================================================================
# 8. INFORMAÇÕES DO BUILD
# =============================================================================
show_info() {
    print_header "📋 Informações do Build"
    
    # Lê versão do pyproject.toml
    VERSION=$(grep "^version" pyproject.toml | cut -d'"' -f2)
    NAME=$(grep "^name" pyproject.toml | cut -d'"' -f2)
    
    echo -e "${GREEN}Pacote:${NC} $NAME"
    echo -e "${GREEN}Versão:${NC} $VERSION"
    echo -e "${GREEN}Diretório:${NC} $PROJECT_DIR"
    
    if [ -d "dist" ]; then
        echo -e "${GREEN}Arquivos de distribuição:${NC}"
        ls -1 dist/
    fi
    
    echo ""
    echo -e "${BLUE}Para instalar o pacote:${NC}"
    echo -e "  pip install dist/$(basename $(ls dist/*.whl 2>/dev/null | head -1) 2>/dev/null)"
    echo ""
    echo -e "${BLUE}Para instalar em modo desenvolvimento:${NC}"
    echo -e "  pip install -e ."
    echo ""
    echo -e "${BLUE}Para upload ao PyPI (requer credenciais):${NC}"
    echo -e "  twine upload dist/*"
    echo ""
}

# =============================================================================
# MENU PRINCIPAL
# =============================================================================
main() {
    case "${1:-all}" in
        clean)
            clean
            ;;
        
        check)
            check_dependencies
            validate
            ;;
        
        test)
            run_tests
            ;;
        
        build)
            build_package
            ;;
        
        validate)
            validate_package
            ;;
        
        install)
            install_local
            ;;
        
        all)
            clean
            check_dependencies
            validate
            
            # Pergunta se quer rodar testes
            read -p "Rodar testes antes do build? (S/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                run_tests
            fi
            
            build_package
            validate_package
            
            # Pergunta se quer instalar localmente
            read -p "Instalar localmente? (S/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                install_local
            fi
            
            show_info
            ;;
        
        info)
            show_info
            ;;
        
        help|--help|-h)
            echo "Uso: ./build.sh [opção]"
            echo ""
            echo "Opções:"
            echo "  all       - Build completo (limpeza + validação + build) [padrão]"
            echo "  clean     - Limpa arquivos de build"
            echo "  check     - Verifica dependências e valida código"
            echo "  test      - Roda testes"
            echo "  build     - Constrói o pacote"
            echo "  validate  - Valida o pacote construído"
            echo "  install   - Instala localmente em modo desenvolvimento"
            echo "  info      - Mostra informações do build"
            echo "  help      - Mostra esta ajuda"
            exit 0
            ;;
        
        *)
            print_error "Opção inválida: $1"
            echo "Use './build.sh help' para ver as opções disponíveis"
            exit 1
            ;;
    esac
}

# Executa
main "$@"

print_header "✅ Concluído!"

