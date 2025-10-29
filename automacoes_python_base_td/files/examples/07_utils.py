"""
EXEMPLO 7: UTILITÁRIOS
=======================

Funções úteis para manipulação de strings, datas e arquivos.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
"""

from automacoes_python_base_td.utils import (
    # String utils
    slugify,
    truncate,
    capitalize_words,
    remove_accents,
    
    # Date utils
    format_timestamp,
    parse_date,
    days_between,
    
    # File utils
    ensure_dir,
    get_file_size,
    file_exists
)
from automacoes_python_base_td.logger import get_logger
from datetime import datetime

logger = get_logger()

# ====================================================================
# STRING UTILS
# ====================================================================

def exemplo_string_utils():
    """Exemplos de manipulação de strings"""
    logger.info("=== String Utils ===")
    
    # Criar slug (URL-friendly)
    titulo = "Como Instalar Python 3.12 no Ubuntu"
    slug = slugify(titulo)
    logger.info(f"Slug: {slug}")
    # Resultado: como-instalar-python-312-no-ubuntu
    
    # Remover acentos
    texto = "Ação, função, manutenção"
    sem_acentos = remove_accents(texto)
    logger.info(f"Sem acentos: {sem_acentos}")
    # Resultado: Acao, funcao, manutencao
    
    # Truncar texto
    descricao = "Este é um texto muito longo que precisa ser truncado para caber"
    resumo = truncate(descricao, max_length=30)
    logger.info(f"Resumo: {resumo}")
    # Resultado: Este é um texto muito lo...
    
    # Capitalizar palavras
    nome = "joão pedro da silva"
    nome_formatado = capitalize_words(nome)
    logger.info(f"Nome: {nome_formatado}")
    # Resultado: João Pedro Da Silva


# ====================================================================
# DATE UTILS
# ====================================================================

def exemplo_date_utils():
    """Exemplos de manipulação de datas"""
    logger.info("\n=== Date Utils ===")
    
    # Formatar timestamp
    agora = datetime.now()
    data_formatada = format_timestamp(agora, format="%d/%m/%Y %H:%M")
    logger.info(f"Data formatada: {data_formatada}")
    
    # Parse string para datetime
    data_string = "2025-10-29"
    data_obj = parse_date(data_string)
    logger.info(f"Data objeto: {data_obj}")
    
    # Calcular dias entre datas
    data1 = datetime(2025, 10, 1)
    data2 = datetime(2025, 10, 29)
    dias = days_between(data1, data2)
    logger.info(f"Dias entre {data1.date()} e {data2.date()}: {dias} dias")


# ====================================================================
# FILE UTILS
# ====================================================================

def exemplo_file_utils():
    """Exemplos de operações com arquivos"""
    logger.info("\n=== File Utils ===")
    
    # Garantir que diretório existe
    logger.info("Criando diretório...")
    ensure_dir("exports/relatorios/2025")
    logger.info("✅ Diretório garantido!")
    
    # Verificar se arquivo existe
    arquivo = "meu_arquivo.txt"
    if file_exists(arquivo):
        logger.info(f"✅ {arquivo} existe!")
        
        # Obter tamanho do arquivo
        tamanho = get_file_size(arquivo)
        logger.info(f"Tamanho: {tamanho} bytes")
    else:
        logger.info(f"❌ {arquivo} não encontrado")


# ====================================================================
# EXEMPLO PRÁTICO 1: Gerar Slug de Produto
# ====================================================================

def criar_slug_produto(nome_produto):
    """
    Cria slug amigável para URL do produto.
    Útil para e-commerce, blogs, etc.
    """
    logger.info(f"\nCriando slug para: {nome_produto}")
    
    # Remover acentos e criar slug
    slug = slugify(remove_accents(nome_produto))
    
    # Truncar se muito longo (máximo 50 caracteres)
    if len(slug) > 50:
        slug = slug[:50].rstrip('-')
    
    logger.info(f"Slug gerado: {slug}")
    logger.info(f"URL: /produtos/{slug}")
    
    return slug


# ====================================================================
# EXEMPLO PRÁTICO 2: Processar Exportação CSV
# ====================================================================

def processar_export_csv():
    """
    Processa exportação de CSV com nomenclatura padronizada.
    Útil para ETL, relatórios, backups.
    """
    logger.info("\n=== Processando Export CSV ===")
    
    # Criar diretório de exports
    export_dir = "exports/vendas"
    ensure_dir(export_dir)
    logger.info(f"✅ Diretório: {export_dir}")
    
    # Gerar nome do arquivo com data
    hoje = format_timestamp(datetime.now(), format="%Y%m%d")
    filename = f"vendas_{hoje}.csv"
    filepath = f"{export_dir}/{filename}"
    
    logger.info(f"📄 Arquivo: {filename}")
    
    # Simular criação do arquivo
    # with open(filepath, 'w') as f:
    #     f.write("id,produto,valor\n")
    #     f.write("1,Notebook,3500.00\n")
    
    # Verificar se foi criado
    if file_exists(filepath):
        tamanho = get_file_size(filepath)
        logger.info(f"✅ Arquivo criado: {filename} ({tamanho} bytes)")
    
    return filepath


# ====================================================================
# EXEMPLO PRÁTICO 3: Calcular Prazo de Entrega
# ====================================================================

def calcular_prazo_entrega(dias_uteis):
    """
    Calcula data de entrega baseado em dias úteis.
    Útil para e-commerce, logística.
    """
    logger.info(f"\n=== Calculando Prazo de Entrega ===")
    logger.info(f"Dias úteis: {dias_uteis}")
    
    hoje = datetime.now()
    
    # Simples: soma dias (em produção, considerar dias úteis)
    data_entrega = datetime(
        hoje.year, 
        hoje.month, 
        hoje.day + dias_uteis
    )
    
    dias_restantes = days_between(hoje, data_entrega)
    data_formatada = format_timestamp(data_entrega, format="%d/%m/%Y")
    
    logger.info(f"📅 Data de entrega: {data_formatada}")
    logger.info(f"⏰ Dias restantes: {dias_restantes}")
    
    return {
        "data": data_formatada,
        "dias": dias_restantes
    }


# ====================================================================
# EXEMPLO PRÁTICO 4: Formatar Nome de Cliente
# ====================================================================

def formatar_nome_cliente(nome):
    """
    Formata nome de cliente para exibição.
    Útil para relatórios, emails, interfaces.
    """
    logger.info(f"\nFormatando nome: {nome}")
    
    # Remover acentos (para algumas situações)
    # nome_sem_acentos = remove_accents(nome)
    
    # Capitalizar corretamente
    nome_formatado = capitalize_words(nome.lower())
    
    logger.info(f"Nome formatado: {nome_formatado}")
    
    return nome_formatado


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("=== Exemplos de Utilitários ===")
    logger.info("=" * 60)
    
    # 1. String Utils
    exemplo_string_utils()
    
    # 2. Date Utils
    exemplo_date_utils()
    
    # 3. File Utils
    exemplo_file_utils()
    
    # 4. Casos Práticos
    logger.info("\n" + "=" * 60)
    logger.info("=== Casos Práticos ===")
    logger.info("=" * 60)
    
    # Slug de produto
    criar_slug_produto("Notebook Dell Inspiron 15 3000 - Intel Core i5")
    
    # Processar export
    processar_export_csv()
    
    # Prazo de entrega
    calcular_prazo_entrega(5)
    
    # Formatar nome
    formatar_nome_cliente("JOÃO PEDRO DA SILVA")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Todos os exemplos concluídos!")
    logger.info("=" * 60)
