import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock

from src.services.seo.analytics import SEOAnalyticsService
from src.models.seo import SiteMetrics


@pytest.fixture
def storage_service():
    return Mock(
        get_latest_metrics=AsyncMock(),
        get_metrics_history=AsyncMock()
    )


@pytest.fixture
def analytics_service(storage_service):
    return SEOAnalyticsService(storage_service)


@pytest.mark.asyncio
async def test_analyze_metrics_empty(analytics_service, storage_service):
    storage_service.get_latest_metrics.return_value = None
    metrics = await analytics_service.analyze_metrics("site1")
    assert metrics == {}


@pytest.mark.asyncio
async def test_generate_insights_empty(analytics_service, storage_service):
    storage_service.get_latest_metrics.return_value = None
    insights, recommendations = await analytics_service.generate_insights("site1")
    assert insights == []
    assert recommendations == []


@pytest.mark.asyncio
async def test_compute_trends_empty(analytics_service, storage_service):
    storage_service.get_metrics_history.return_value = []
    trends = await analytics_service.compute_trends("site1", 30)
    assert trends == []