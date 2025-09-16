"""Configuration management with environment-specific settings."""

import os
from functools import lru_cache
from typing import Any, Dict

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings with validation and type checking."""
    
    # Application
    app_name: str = "Distributed Task System"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/taskdb"
    database_pool_size: int = 20
    database_max_overflow: int = 30
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 100
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Monitoring
    prometheus_port: int = 8001
    log_level: str = "INFO"
    
    # Circuit Breaker
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_timeout: int = 60
    
    @validator("database_url")
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Invalid database URL format")
        return v
    
    @validator("environment")
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "testing", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


class FeatureFlags:
    """Dynamic feature flags with configuration."""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self._cache: Dict[str, Any] = {}
    
    async def is_enabled(self, feature: str, user_id: str = None) -> bool:
        """Check if a feature is enabled for a user."""
        return self._cache.get(feature, False)
    
    async def set_flag(self, feature: str, enabled: bool) -> None:
        """Set a feature flag."""
        self._cache[feature] = enabled
        if self.redis_client:
            await self.redis_client.set(f"feature:{feature}", str(enabled))