"""Integration tests for API endpoints."""

import pytest
from httpx import AsyncClient

from src.api.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health check endpoints."""
    
    async def test_health_check(self):
        """Test health check endpoint."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "timestamp" in data
    
    async def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/metrics")
            
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]


@pytest.mark.asyncio
class TestErrorHandling:
    """Test error handling in API."""
    
    async def test_404_handling(self):
        """Test 404 error handling."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/nonexistent")
            
            assert response.status_code == 404