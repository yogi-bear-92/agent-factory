"""Tests for SEO processor service."""

from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl

from src.models.seo import CrawlJob, CrawlStatus, DataSource, SEOMetrics
from src.services.seo.processor import SEOProcessorService


@pytest.fixture
def processor():
    """Create processor service fixture."""
    return SEOProcessorService()


@pytest.fixture
def valid_metrics():
    """Create valid SEO metrics fixture."""
    return SEOMetrics(
        url=HttpUrl("https://example.com"),
        title="Test Page",
        description="Test description",
        rank_position=1,
        visibility_score=85.0,
        page_authority=60.0,
        backlinks_count=100,
        organic_traffic=1000,
        keyword_rankings={"test": 5},
        performance_metrics={"speed_index": 2.5},
        last_updated=datetime.now(UTC),
    )


@pytest.fixture
def invalid_metrics():
    """Create SEO metrics fixture with values to normalize."""
    return {
        "url": "https://example.com",
        "title": "Test Page",
        "description": "Test description",
        "rank_position": 1,
        "visibility_score": 150.0,  # Over max threshold
        "page_authority": 120.0,    # Over max threshold
        "backlinks_count": -5,      # Invalid negative value
        "organic_traffic": -10,     # Invalid negative value
        "keyword_rankings": {"test": 0},  # Invalid rank
        "performance_metrics": {"speed_index": 2.5},
        "last_updated": datetime.now(UTC),
    }


@pytest.fixture
def crawl_job(valid_metrics):
    """Create sample crawl job fixture."""
    return CrawlJob(
        url=valid_metrics.url,
        data_source=DataSource.GOOGLE,
        status=CrawlStatus.PENDING,
        priority=50,
    )


async def test_normalize_metrics(processor, valid_metrics):
    """Test metrics normalization."""
    # Create metrics with invalid values
    metrics = SEOMetrics(
        url=HttpUrl("https://example.com"),
        title="Test Page",
        description="Test description",
        rank_position=1,
        visibility_score=85.0,
        page_authority=60.0,
        backlinks_count=100,
        organic_traffic=1000,
        keyword_rankings={"test": 5},
        performance_metrics={"speed_index": 2.5},
        last_updated=datetime.now(UTC),
    )
    metrics.visibility_score = 150.0  # Over max threshold
    metrics.page_authority = 120.0   # Over max threshold
    metrics.backlinks_count = -5     # Invalid negative value
    metrics.organic_traffic = -10    # Invalid negative value
    metrics.keyword_rankings = {"test": 0}  # Invalid rank

    normalized = await processor._normalize_metrics(metrics)

    assert normalized.visibility_score <= 100.0
    assert normalized.page_authority <= 100.0
    assert normalized.backlinks_count >= 0
    assert normalized.organic_traffic >= 0
    assert all(rank >= 1 for rank in normalized.keyword_rankings.values())


async def test_process_job(processor, crawl_job, valid_metrics):
    """Test single job processing."""
    result = await processor._process_job(crawl_job)

    assert result is not None
    assert isinstance(result, SEOMetrics)
    assert crawl_job.status == CrawlStatus.COMPLETED
    assert crawl_job.metrics == result


async def test_process_jobs_batch(processor, crawl_job):
    """Test batch job processing."""
    jobs = [crawl_job for _ in range(5)]
    result = await processor.process_jobs(jobs)

    assert result.success
    assert "processed_metrics" in result.output
    assert len(result.output["processed_metrics"]) == 5
    assert all(job.status == CrawlStatus.COMPLETED for job in jobs)