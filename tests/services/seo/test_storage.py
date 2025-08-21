"""Tests for SEO storage service."""

from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl

from src.models.seo import SEOMetrics
from src.services.seo.storage import SEOStorageService


@pytest.fixture
def storage():
    """Create storage service fixture."""
    return SEOStorageService()


@pytest.fixture
def seo_metrics():
    """Create sample SEO metrics fixture."""
    return SEOMetrics(
        url=HttpUrl("https://example.com"),
        title="Test Page",
        description="Test description",
        rank_position=1,
        visibility_score=85.5,
        page_authority=60.0,
        backlinks_count=1000,
        organic_traffic=5000,
        keyword_rankings={"test": 1},
        performance_metrics={"speed_index": 2.5},
        last_updated=datetime.now(UTC),
    )


async def test_store_single_metric(storage, seo_metrics):
    """Test storing single metrics."""
    result = await storage.store_metrics(seo_metrics)

    assert result.success
    assert result.output["stored_count"] == 1


async def test_store_multiple_metrics(storage, seo_metrics):
    """Test storing multiple metrics."""
    metrics = [seo_metrics for _ in range(3)]
    result = await storage.store_metrics(metrics)

    assert result.success
    assert result.output["stored_count"] == 3


async def test_query_metrics(storage, seo_metrics):
    """Test querying metrics."""
    # Store test data
    await storage.store_metrics(seo_metrics)

    # Query with filters
    result = await storage.query_metrics(
        url=str(seo_metrics.url),
        min_authority=50.0,
        min_visibility=80.0,
    )

    assert result.success
    assert len(result.output["metrics"]) > 0

    metrics = result.output["metrics"][0]
    assert isinstance(metrics, SEOMetrics)
    assert metrics.url == seo_metrics.url
