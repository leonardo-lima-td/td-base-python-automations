"""
Testes para configurações unificadas
Testa funcionalidade do Pydantic Settings v2
"""
import pytest
import os
from automacoes_python_base_td.settings import AppSettings, settings


class TestAppSettings:
    """Testes para AppSettings unificado"""
    
    def test_import_settings(self):
        """Testa importação do settings global"""
        from automacoes_python_base_td.settings import settings
        
        assert settings is not None
        assert isinstance(settings, AppSettings)
    
    def test_default_values(self, monkeypatch):
        """Testa valores padrão"""
        # Forçar valores padrão sem variáveis de ambiente
        test_settings = AppSettings(
            env="dev",
            debug_mode=False,
            app_name="td-base-python-automations",
            db_host="localhost",
            db_user="test",
            db_password="test"
        )
        
        assert test_settings.env == "dev"
        assert test_settings.debug_mode is False
        assert test_settings.app_name == "td-base-python-automations"
    
    def test_custom_values(self, monkeypatch):
        """Testa valores customizados via env vars"""
        monkeypatch.setenv("ENV", "prd")
        monkeypatch.setenv("DEBUG_MODE", "true")
        monkeypatch.setenv("APP_NAME", "My App")
        monkeypatch.setenv("DB_HOST", "prod-db")
        monkeypatch.setenv("DB_USER", "prod_user")
        monkeypatch.setenv("DB_PASSWORD", "prod_pass")
        
        test_settings = AppSettings()
        
        assert test_settings.env == "prd"
        assert test_settings.debug_mode is True
        assert test_settings.app_name == "My App"
    
    def test_case_insensitive(self, monkeypatch):
        """Testa se env vars são case insensitive"""
        monkeypatch.setenv("env", "staging")
        monkeypatch.setenv("db_host", "test-db")
        monkeypatch.setenv("db_user", "user")
        monkeypatch.setenv("db_password", "pass")
        
        test_settings = AppSettings()
        
        assert test_settings.env == "staging"
        assert test_settings.db_host == "test-db"
    
    def test_computed_fields(self, monkeypatch):
        """Testa campos computados"""
        monkeypatch.setenv("DB_HOST", "test-db")
        monkeypatch.setenv("DB_USER", "testuser")
        monkeypatch.setenv("DB_PASSWORD", "testpass")
        monkeypatch.setenv("DB_PORT", "5432")
        
        test_settings = AppSettings()
        
        # Testa URLs computadas (database_url, não postgres_url)
        assert "postgresql://" in test_settings.database_url
        assert "testuser" in test_settings.database_url
        assert "test-db" in test_settings.database_url
        
        # Testa TDAX URL
        assert "postgresql://" in test_settings.database_url_tdax
        assert "tdax" in test_settings.database_url_tdax
        
        # Testa Automations URL
        assert "postgresql://" in test_settings.database_url_automation
        assert "automacoes" in test_settings.database_url_automation
    
    def test_debug_mode_affects_log_level(self, monkeypatch):
        """Testa se debug_mode afeta effective_log_level"""
        monkeypatch.setenv("DB_HOST", "test")
        monkeypatch.setenv("DB_USER", "test")
        monkeypatch.setenv("DB_PASSWORD", "test")
        
        # Sem debug
        monkeypatch.setenv("DEBUG_MODE", "false")
        monkeypatch.setenv("LOG_LEVEL", "INFO")
        settings1 = AppSettings()
        assert settings1.effective_log_level == "INFO"
        
        # Com debug
        monkeypatch.setenv("DEBUG_MODE", "true")
        settings2 = AppSettings()
        assert settings2.effective_log_level == "DEBUG"
    
    def test_use_cloudwatch_logic(self, monkeypatch):
        """Testa lógica de uso do CloudWatch"""
        monkeypatch.setenv("DB_HOST", "test")
        monkeypatch.setenv("DB_USER", "test")
        monkeypatch.setenv("DB_PASSWORD", "test")
        
        # Dev não usa CloudWatch
        monkeypatch.setenv("ENV", "dev")
        monkeypatch.setenv("CLOUDWATCH_REGION", "us-east-1")
        settings1 = AppSettings()
        assert settings1.use_cloudwatch is False
        
        # Prod usa CloudWatch se configurado
        monkeypatch.setenv("ENV", "prd")
        monkeypatch.setenv("CLOUDWATCH_REGION", "us-east-1")
        settings2 = AppSettings()
        assert settings2.use_cloudwatch is True
    
    def test_rabbit_usage_validation(self, monkeypatch):
        """Testa validação condicional do RabbitMQ"""
        monkeypatch.setenv("DB_HOST", "test")
        monkeypatch.setenv("DB_USER", "test")
        monkeypatch.setenv("DB_PASSWORD", "test")
        
        # Com rabbit_usage=False, variáveis são opcionais
        monkeypatch.setenv("RABBIT_USAGE", "false")
        settings1 = AppSettings()
        assert settings1.rabbit_usage is False
        
        # Com rabbit_usage=True, deve validar (vai falhar sem as variáveis)
        monkeypatch.setenv("RABBIT_USAGE", "true")
        with pytest.raises(ValueError, match="rabbit_usage"):
            AppSettings()
    
    def test_log_stream_name_format(self, monkeypatch):
        """Testa formato do log stream name"""
        monkeypatch.setenv("APP_NAME", "Test App")
        monkeypatch.setenv("ENV", "prd")
        monkeypatch.setenv("DB_HOST", "test")
        monkeypatch.setenv("DB_USER", "test")
        monkeypatch.setenv("DB_PASSWORD", "test")
        
        test_settings = AppSettings()
        
        # Deve ser formato: app-slug-env-DDMMYYYY
        stream_name = test_settings.log_stream_name
        assert "test-app" in stream_name
        assert "prd" in stream_name
        assert len(stream_name.split("-")[-1]) == 8  # Data DDMMYYYY
    
    def test_environment_helpers(self, monkeypatch):
        """Testa helpers de ambiente"""
        monkeypatch.setenv("DB_HOST", "test")
        monkeypatch.setenv("DB_USER", "test")
        monkeypatch.setenv("DB_PASSWORD", "test")
        
        # Dev
        monkeypatch.setenv("ENV", "dev")
        settings1 = AppSettings()
        assert settings1.is_development is True
        assert settings1.is_production is False
        assert settings1.is_staging is False
        
        # Production
        monkeypatch.setenv("ENV", "prd")
        settings2 = AppSettings()
        assert settings2.is_development is False
        assert settings2.is_production is True
        assert settings2.is_staging is False
        
        # Staging
        monkeypatch.setenv("ENV", "staging")
        settings3 = AppSettings()
        assert settings3.is_development is False
        assert settings3.is_production is False
        assert settings3.is_staging is True

