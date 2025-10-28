"""
Utilitários para manipulação de arquivos e diretórios
"""
import os
import shutil
from typing import List, Optional
from pathlib import Path


def listdir(path: str, filter_ext: Optional[str] = None) -> List[str]:
    """
    Lista arquivos e diretórios em um caminho.
    
    Args:
        path: Caminho do diretório
        filter_ext: Extensão para filtrar (ex: '.txt', '.csv')
    
    Returns:
        Lista de nomes de arquivos/diretórios
    
    Exemplo:
        files = listdir('/path/to/dir')
        csv_files = listdir('/path/to/dir', filter_ext='.csv')
    """
    if not os.path.exists(path):
        return []
    
    items = os.listdir(path)
    
    if filter_ext:
        items = [item for item in items if item.endswith(filter_ext)]
    
    return items


def getdir(path: str) -> str:
    """
    Retorna o diretório de um caminho de arquivo.
    
    Args:
        path: Caminho do arquivo
    
    Returns:
        Caminho do diretório
    
    Exemplo:
        dir_path = getdir('/path/to/file.txt')  # '/path/to'
    """
    return os.path.dirname(path)


def openfile(path: str, mode: str = 'r', encoding: str = 'utf-8'):
    """
    Abre um arquivo.
    
    Args:
        path: Caminho do arquivo
        mode: Modo de abertura ('r', 'w', 'a', 'rb', 'wb')
        encoding: Codificação (default: 'utf-8')
    
    Returns:
        File object
    
    Exemplo:
        with openfile('/path/file.txt', 'r') as f:
            content = f.read()
    """
    if 'b' in mode:
        return open(path, mode)
    return open(path, mode, encoding=encoding)


def getsize(path: str) -> int:
    """
    Retorna o tamanho de um arquivo em bytes.
    
    Args:
        path: Caminho do arquivo
    
    Returns:
        Tamanho em bytes
    
    Exemplo:
        size = getsize('/path/file.txt')
        size_mb = size / (1024 * 1024)
    """
    if not os.path.exists(path):
        return 0
    return os.path.getsize(path)


def exists(path: str) -> bool:
    """
    Verifica se um arquivo ou diretório existe.
    
    Args:
        path: Caminho do arquivo ou diretório
    
    Returns:
        True se existe, False caso contrário
    
    Exemplo:
        if exists('/path/file.txt'):
            print("Arquivo existe!")
    """
    return os.path.exists(path)


def isfile(path: str) -> bool:
    """
    Verifica se o caminho é um arquivo.
    
    Args:
        path: Caminho a verificar
    
    Returns:
        True se é arquivo, False caso contrário
    """
    return os.path.isfile(path)


def isdir(path: str) -> bool:
    """
    Verifica se o caminho é um diretório.
    
    Args:
        path: Caminho a verificar
    
    Returns:
        True se é diretório, False caso contrário
    """
    return os.path.isdir(path)


def create_dir(path: str, exist_ok: bool = True) -> bool:
    """
    Cria um diretório.
    
    Args:
        path: Caminho do diretório
        exist_ok: Se True, não gera erro se diretório já existe
    
    Returns:
        True se criado com sucesso
    
    Exemplo:
        create_dir('/path/to/new/dir')
    """
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")
        return False


def remove_file(path: str) -> bool:
    """
    Remove um arquivo.
    
    Args:
        path: Caminho do arquivo
    
    Returns:
        True se removido com sucesso
    
    Exemplo:
        remove_file('/path/file.txt')
    """
    try:
        if os.path.exists(path):
            os.remove(path)
        return True
    except Exception as e:
        print(f"Erro ao remover arquivo: {e}")
        return False


def remove_dir(path: str, recursive: bool = False) -> bool:
    """
    Remove um diretório.
    
    Args:
        path: Caminho do diretório
        recursive: Se True, remove diretório e todo seu conteúdo
    
    Returns:
        True se removido com sucesso
    
    Exemplo:
        remove_dir('/path/to/dir', recursive=True)
    """
    try:
        if os.path.exists(path):
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
        return True
    except Exception as e:
        print(f"Erro ao remover diretório: {e}")
        return False


def copy_file(src: str, dst: str) -> bool:
    """
    Copia um arquivo.
    
    Args:
        src: Caminho do arquivo origem
        dst: Caminho do arquivo destino
    
    Returns:
        True se copiado com sucesso
    
    Exemplo:
        copy_file('/path/file.txt', '/path/file_backup.txt')
    """
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"Erro ao copiar arquivo: {e}")
        return False


def move_file(src: str, dst: str) -> bool:
    """
    Move um arquivo.
    
    Args:
        src: Caminho do arquivo origem
        dst: Caminho do arquivo destino
    
    Returns:
        True se movido com sucesso
    
    Exemplo:
        move_file('/path/file.txt', '/new/path/file.txt')
    """
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(f"Erro ao mover arquivo: {e}")
        return False


def read_file(path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Lê o conteúdo de um arquivo.
    
    Args:
        path: Caminho do arquivo
        encoding: Codificação (default: 'utf-8')
    
    Returns:
        Conteúdo do arquivo ou None se erro
    
    Exemplo:
        content = read_file('/path/file.txt')
        if content:
            print(content)
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None


def write_file(path: str, content: str, mode: str = 'w', encoding: str = 'utf-8') -> bool:
    """
    Escreve conteúdo em um arquivo.
    
    Args:
        path: Caminho do arquivo
        content: Conteúdo a escrever
        mode: Modo de escrita ('w' para sobrescrever, 'a' para adicionar)
        encoding: Codificação (default: 'utf-8')
    
    Returns:
        True se escrito com sucesso
    
    Exemplo:
        write_file('/path/file.txt', 'Hello World!')
        write_file('/path/file.txt', 'Append text', mode='a')
    """
    try:
        # Cria diretório se não existe
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        with open(path, mode, encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo: {e}")
        return False

