"""
Testes para utilitários de data
Testa funcionalidade e edge cases
"""
import pytest
from datetime import datetime
from automacoes_python_base_td.utils.date_utils import (
    format_timestamp,
    parse_date,
    days_between,
)


class TestFormatTimestamp:
    """Testes para função format_timestamp"""
    
    def test_format_timestamp_default(self):
        """Testa formatação com formato padrão"""
        dt = datetime(2025, 10, 28, 14, 30, 45)
        result = format_timestamp(dt)
        assert result == "2025-10-28 14:30:45"
    
    def test_format_timestamp_custom_format(self):
        """Testa formatação com formato customizado"""
        dt = datetime(2025, 10, 28, 14, 30, 45)
        result = format_timestamp(dt, format="%d/%m/%Y")
        assert result == "28/10/2025"
    
    def test_format_timestamp_none_uses_now(self):
        """Testa formatação sem data (usa data atual)"""
        result = format_timestamp()
        # Verifica se retornou uma string no formato correto
        assert len(result) == 19  # "YYYY-MM-DD HH:MM:SS"
        assert result[4] == "-"
        assert result[7] == "-"
        assert result[10] == " "


class TestParseDate:
    """Testes para função parse_date"""
    
    def test_parse_date_valid_string(self):
        """Testa parse de string válida"""
        result = parse_date("2025-10-28")
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 10
        assert result.day == 28
    
    def test_parse_date_custom_format(self):
        """Testa parse com formato customizado"""
        result = parse_date("28/10/2025", format="%d/%m/%Y")
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 10
        assert result.day == 28
    
    def test_parse_date_invalid_string(self):
        """Testa parse de string inválida"""
        result = parse_date("invalid-date")
        assert result is None
    
    def test_parse_date_empty_string(self):
        """Testa parse de string vazia"""
        result = parse_date("")
        assert result is None


class TestDaysBetween:
    """Testes para função days_between"""
    
    def test_days_between_same_day(self):
        """Testa dias entre mesma data"""
        dt1 = datetime(2025, 10, 28)
        dt2 = datetime(2025, 10, 28)
        result = days_between(dt1, dt2)
        assert result == 0
    
    def test_days_between_different_days(self):
        """Testa dias entre datas diferentes"""
        dt1 = datetime(2025, 10, 28)
        dt2 = datetime(2025, 11, 2)
        result = days_between(dt1, dt2)
        assert result == 5
    
    def test_days_between_reverse_order(self):
        """Testa dias entre datas em ordem inversa"""
        dt1 = datetime(2025, 11, 2)
        dt2 = datetime(2025, 10, 28)
        result = days_between(dt1, dt2)
        assert result == -5
    
    def test_days_between_with_time(self):
        """Testa dias entre datas com hora"""
        dt1 = datetime(2025, 10, 28, 14, 30)
        dt2 = datetime(2025, 10, 29, 10, 15)
        result = days_between(dt1, dt2)
        # Deve considerar apenas os dias, não as horas
        assert result == 1

