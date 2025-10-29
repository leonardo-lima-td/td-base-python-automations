"""
Exemplo de uso dos Utils (File, String, Date)
"""
from automacoes_python_base_td import (
    # File utils
    create_dir, exists, isfile, isdir, read_file, write_file,
    copy_file, move_file, remove_file, listdir,
    # String utils
    slugify, truncate, capitalize_words,
    # Date utils
    format_timestamp, parse_date, days_between,
    # Logger
    logger
)
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger.info("=== Exemplo de Utils ===")

# ===================================
# File Utils
# ===================================
logger.info("\n### File Utils ###")

# Criar diretório
# create_dir("temp_folder")
# logger.success("Diretório 'temp_folder' criado")

# Verificar existência
logger.info(f"Arquivo main.py existe? {exists('main.py')}")
logger.info(f"É arquivo? {isfile('main.py')}")
logger.info(f"É diretório? {isdir('venv')}")

# Escrever arquivo
# write_file("temp_folder/teste.txt", "Conteúdo de teste\nLinha 2\nLinha 3")
# logger.success("Arquivo escrito com sucesso")

# Ler arquivo
# conteudo = read_file("temp_folder/teste.txt")
# logger.info(f"Conteúdo lido:\n{conteudo}")

# Listar arquivos
arquivos_raiz = listdir(".")
logger.info(f"Arquivos na raiz (primeiros 5): {arquivos_raiz[:5]}")

# Copiar arquivo
# copy_file("temp_folder/teste.txt", "temp_folder/teste_copia.txt")
# logger.success("Arquivo copiado")

# Mover arquivo
# move_file("temp_folder/teste_copia.txt", "temp_folder/teste_movido.txt")
# logger.success("Arquivo movido")

# Remover arquivo
# remove_file("temp_folder/teste_movido.txt")
# logger.success("Arquivo removido")

# ===================================
# String Utils
# ===================================
logger.info("\n### String Utils ###")

# Slugify - converter texto para slug
texto = "Olá Mundo! Este é um teste 123"
slug = slugify(texto)
logger.info(f"Original: {texto}")
logger.info(f"Slug: {slug}")

# Truncate - truncar texto
texto_longo = "Este é um texto muito longo que precisa ser truncado para caber em um espaço limitado"
texto_truncado = truncate(texto_longo, length=30)
logger.info(f"Original: {texto_longo}")
logger.info(f"Truncado: {texto_truncado}")

# Capitalize words - capitalizar palavras
texto_lowercase = "joão da silva santos"
texto_capitalizado = capitalize_words(texto_lowercase)
logger.info(f"Original: {texto_lowercase}")
logger.info(f"Capitalizado: {texto_capitalizado}")

# ===================================
# Date Utils
# ===================================
logger.info("\n### Date Utils ###")

# Format timestamp - formatar timestamp
agora = datetime.now()
timestamp_formatado = format_timestamp(agora, format="%d/%m/%Y %H:%M:%S")
logger.info(f"Data/hora formatada: {timestamp_formatado}")

# Parse date - converter string para date
data_string = "2025-10-29"
data_objeto = parse_date(data_string, format="%Y-%m-%d")
logger.info(f"String '{data_string}' convertida para: {data_objeto}")

# Days between - dias entre duas datas
data1 = datetime(2025, 10, 1)
data2 = datetime(2025, 10, 29)
diferenca = days_between(data1, data2)
logger.info(f"Dias entre {data1.date()} e {data2.date()}: {diferenca} dias")

logger.success("Todos os exemplos de utils executados!")

