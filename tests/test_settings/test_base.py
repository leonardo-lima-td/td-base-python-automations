"""
Testes para configurações base
Testa funcionalidade do Pydantic Settings
"""
import pytest
import os
from automacoes_python_base_td.settings.base import (
    BaseAppSettings,
    get_settings,
)


class TestBaseAppSettings:
    """Testes para BaseAppSettings"""
    
    def test_default_values(self):
        """Testa valores padrão"""
        settings = BaseAppSettings()
        
        assert settings.env == "development"
        assert settings.debug is False
        assert settings.app_name == "TD App"
    
    def test_custom_values(self, monkeypatch):
        """Testa valores customizados via env vars"""
        monkeypatch.setenv("ENV", "production")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("APP_NAME", "My App")
        
        settings = BaseAppSettings()
        
        assert settings.env == "production"
        assert settings.debug is True
        assert settings.app_name == "My App"
    
    def test_case_insensitive(self, monkeypatch):
        """Testa se env vars são case insensitive"""
        monkeypatch.setenv("env", "staging")
        monkeypatch.setenv("ENV", "production")
        
        settings = BaseAppSettings()
        
        # Deve pegar qualquer variação de case
        assert settings.env in ["staging", "production"]
    
    def test_get_settings_singleton(self):
        """Testa se get_settings retorna singleton"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Deve retornar a mesma instância
        assert settings1 is settings2

