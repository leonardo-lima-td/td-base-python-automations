#!/bin/bash

# Script para rodar os testes do pacote automacoes-python-base-td

echo "========================================="
echo "🧪 TESTES AUTOMACOES-PYTHON-BASE-TD"
echo "========================================="
echo ""

# Verifica se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest não encontrado. Instalando..."
    pip install pytest pytest-cov
fi

echo "📦 Instalando pacote em modo desenvolvimento..."
pip install -e ".[dev]" -q

echo ""
echo "========================================="
echo "🚀 RODANDO TESTES"
echo "========================================="
echo ""

# Opções:
# -v: verbose
# --tb=short: traceback curto
# -ra: mostra resumo de todos os testes
# --cov: cobertura de código
# --cov-report=term-missing: mostra linhas não cobertas

case "${1:-all}" in
    "all")
        echo "✅ Rodando TODOS os testes..."
        pytest tests/ -v --tb=short -ra
        ;;
    
    "core")
        echo "✅ Rodando testes de CORE (exceptions)..."
        pytest tests/test_core/ -v --tb=short
        ;;
    
    "database")
        echo "✅ Rodando testes de DATABASE..."
        pytest tests/test_database/ -v --tb=short
        ;;
    
    "aws")
        echo "✅ Rodando testes de AWS..."
        pytest tests/test_aws/ -v --tb=short
        ;;
    
    "rabbitmq")
        echo "✅ Rodando testes de RABBITMQ..."
        pytest tests/test_rabbitmq/ -v --tb=short
        ;;
    
    "utils")
        echo "✅ Rodando testes de UTILS..."
        pytest tests/test_utils/ -v --tb=short
        ;;
    
    "settings")
        echo "✅ Rodando testes de SETTINGS..."
        pytest tests/test_settings/ -v --tb=short
        ;;
    
    "logger")
        echo "✅ Rodando testes de LOGGER..."
        pytest tests/test_logger/ -v --tb=short
        ;;
    
    "coverage")
        echo "✅ Rodando testes com COBERTURA..."
        pytest tests/ -v --cov=automacoes_python_base_td --cov-report=html --cov-report=term-missing
        echo ""
        echo "📊 Relatório de cobertura gerado em: htmlcov/index.html"
        ;;
    
    *)
        echo "❌ Opção inválida: $1"
        echo ""
        echo "Uso: ./run_tests.sh [opção]"
        echo ""
        echo "Opções disponíveis:"
        echo "  all        - Todos os testes (padrão)"
        echo "  core       - Testes de exceções"
        echo "  database   - Testes de database"
        echo "  aws        - Testes de AWS"
        echo "  rabbitmq   - Testes de RabbitMQ"
        echo "  utils      - Testes de utilitários"
        echo "  settings   - Testes de settings"
        echo "  logger     - Testes de logger"
        echo "  coverage   - Todos os testes + cobertura"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "✅ TESTES FINALIZADOS"
echo "========================================="

