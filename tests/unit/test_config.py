"""Unit tests for configuration module."""

import pytest
from pydantic import ValidationError

from src.core.config import Settings, FeatureFlags


class TestSettings:
    """Test cases for Settings class."""
    
    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        
        assert settings.app_name == "Distributed Task System"
        assert settings.version == "1.0.0"
        assert settings.debug is False
        assert settings.environment == "production"
        assert settings.api_port == 8000
        assert settings.rate_limit_per_minute == 60
    
    def test_database_url_validation(self):
        """Test database URL validation."""
        # Valid URLs
        valid_urls = [
            "postgresql://user:pass@localhost:5432/db",
            "postgresql+asyncpg://user:pass@localhost:5432/db"
        ]
        
        for url in valid_urls:
            settings = Settings(database_url=url)
            assert settings.database_url == url
        
        # Invalid URL
        with pytest.raises(ValidationError):
            Settings(database_url="invalid://url")
    
    def test_environment_validation(self):
        """Test environment validation."""
        # Valid environments
        valid_envs = ["development", "testing", "staging", "production"]
        
        for env in valid_envs:
            settings = Settings(environment=env)
            assert settings.environment == env
        
        # Invalid environment
        with pytest.raises(ValidationError):
            Settings(environment="invalid")


class TestFeatureFlags:
    """Test cases for FeatureFlags class."""
    
    @pytest.mark.asyncio
    async def test_feature_flag_operations(self):
        """Test feature flag set and get operations."""
        flags = FeatureFlags()
        
        # Test setting and getting flag
        await flags.set_flag("new_feature", True)
        assert await flags.is_enabled("new_feature") is True
        
        # Test disabled flag
        await flags.set_flag("disabled_feature", False)
        assert await flags.is_enabled("disabled_feature") is False
        
        # Test non-existent flag
        assert await flags.is_enabled("non_existent") is False