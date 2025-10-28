"""
Utilitários para manipulação de datas
"""
from datetime import datetime
from typing import Optional


def format_timestamp(
    dt: Optional[datetime] = None,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Formata uma data/hora para string.
    
    Args:
        dt: Data/hora a ser formatada (default: agora)
        format: Formato da string (default: YYYY-MM-DD HH:MM:SS)
    
    Returns:
        String formatada
    
    Exemplo:
        timestamp = format_timestamp()
        date_only = format_timestamp(format="%Y-%m-%d")
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format)


def parse_date(date_string: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Converte uma string para datetime.
    
    Args:
        date_string: String com a data
        format: Formato da string (default: YYYY-MM-DD)
    
    Returns:
        Objeto datetime ou None se erro
    
    Exemplo:
        date = parse_date("2025-10-28")
        date = parse_date("28/10/2025", format="%d/%m/%Y")
    """
    try:
        return datetime.strptime(date_string, format)
    except Exception as e:
        print(f"Erro ao fazer parse da data: {e}")
        return None


def days_between(date1: datetime, date2: datetime) -> int:
    """
    Calcula o número de dias entre duas datas.
    
    Args:
        date1: Data inicial
        date2: Data final
    
    Returns:
        Número de dias
    
    Exemplo:
        from datetime import datetime
        d1 = datetime(2025, 10, 1)
        d2 = datetime(2025, 10, 28)
        days = days_between(d1, d2)  # 27
    """
    delta = date2 - date1
    return abs(delta.days)

