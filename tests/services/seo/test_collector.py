"""Tests for SEO collector service."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import HttpUrl

from src.models.seo import CrawlJob, CrawlStatus, DataSource, SEOMetrics
from src.services.seo.collector import SEOCollectorService


@pytest.fixture
def collector() -> SEOCollectorService:
    """Create a collector service instance."""
    collector = SEOCollectorService()
    collector.backoff_base = 0.1  # Speed up tests
    return collector


@pytest.fixture
def crawl_job() -> CrawlJob:
    """Create a sample crawl job."""
    return CrawlJob(
        url=HttpUrl("https://example.com"),
        data_source=DataSource.GOOGLE,
        priority=50,
        depth=1,
    )


@pytest.fixture
def test_metrics(crawl_job: CrawlJob) -> SEOMetrics:
    """Create test metrics."""
    return SEOMetrics(
        url=crawl_job.url,
        title="Test Page",
        description="Test Description",
        rank_position=1,
        visibility_score=75.0,
        page_authority=60.0,
        backlinks_count=100,
        organic_traffic=1000,
        keyword_rankings={"test": 1},
        performance_metrics={"speed_index": 2.5},
        last_updated=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_collect_metrics_success(
    collector: SEOCollectorService,
    crawl_job: CrawlJob,
    test_metrics: SEOMetrics,
) -> None:
    """Test successful metrics collection."""
    mock_collect = AsyncMock(return_value=test_metrics)
    with patch.object(collector, "_collect_from_source", new=mock_collect):
        result = await collector.collect_metrics(crawl_job)

        assert result.success
        assert "metrics" in result.output
        assert isinstance(result.output["metrics"], dict)
        assert crawl_job.status == CrawlStatus.COMPLETED
        assert crawl_job.metrics is not None
        assert isinstance(crawl_job.metrics, SEOMetrics)
        assert crawl_job.error_message is None
        assert crawl_job.metrics.title == test_metrics.title
        mock_collect.assert_called_once_with(crawl_job)


@pytest.mark.asyncio
async def test_handle_rate_limiting(collector: SEOCollectorService) -> None:
    """Test rate limiting behavior."""
    start_time = datetime.now(UTC)
    await collector._handle_rate_limiting(DataSource.GOOGLE)
    end_time = datetime.now(UTC)

    # Should wait at least 1/rate_limit seconds
    expected_min_delay = 1.0 / collector.rate_limits[DataSource.GOOGLE]
    actual_delay = (end_time - start_time).total_seconds()

    assert actual_delay >= expected_min_delay


@pytest.mark.asyncio
async def test_collect_metrics_with_retry(
    collector: SEOCollectorService,
    crawl_job: CrawlJob,
    test_metrics: SEOMetrics,
) -> None:
    """Test metrics collection with retry logic."""
    mock_collect = AsyncMock()
    mock_collect.side_effect = [Exception("Temporary failure"), test_metrics]

    with patch.object(collector, "_collect_from_source", new=mock_collect):
        result = await collector.collect_metrics(crawl_job)

        assert result.success
        assert crawl_job.retry_count == 1
        assert crawl_job.status == CrawlStatus.COMPLETED
        assert crawl_job.metrics == test_metrics
        assert mock_collect.call_count == 2


@pytest.mark.asyncio
async def test_collect_metrics_failure(
    collector: SEOCollectorService,
    crawl_job: CrawlJob,
) -> None:
    """Test metrics collection failure handling."""
    mock_collect = AsyncMock(side_effect=Exception("API error"))

    with patch.object(collector, "_collect_from_source", new=mock_collect):
        result = await collector.collect_metrics(crawl_job)

        assert not result.success
        assert len(result.errors) == 1
        assert "API error" in result.errors[0]
        assert crawl_job.status == CrawlStatus.FAILED
        assert crawl_job.error_message == "API error"
        assert crawl_job.retry_count == collector.max_retries + 1
        assert mock_collect.call_count == collector.max_retries + 1
