import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock

from src.api.rest.app import app
from src.api.seo.dependencies import get_analytics_service
from src.services.seo.analytics import SEOAnalyticsService


@pytest.fixture
def analytics_service():
    return Mock(
        analyze_metrics=AsyncMock(),
        generate_insights=AsyncMock(),
        compute_trends=AsyncMock()
    )


@pytest.fixture
def client(analytics_service):
    app.dependency_overrides = {
        get_analytics_service: lambda: analytics_service
    }
    return TestClient(app)


def test_get_metrics_404(client, analytics_service):
    analytics_service.analyze_metrics.return_value = {}
    response = client.get("/api/v1/seo/sites/site1/metrics")
    assert response.status_code == 404


def test_get_insights_404(client, analytics_service):
    analytics_service.generate_insights.return_value = ([], [])
    response = client.get("/api/v1/seo/sites/site1/insights")
    assert response.status_code == 404


def test_get_trends_404(client, analytics_service):
    analytics_service.compute_trends.return_value = []
    response = client.get("/api/v1/seo/sites/site1/trends")
    assert response.status_code == 404