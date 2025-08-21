"""Tests for SEO queue service."""


import pytest
from pydantic import HttpUrl

from src.models.seo import CrawlJob, CrawlStatus, DataSource
from src.services.seo.queue import SEOQueueService


@pytest.fixture
def queue():
    """Create queue service fixture."""
    return SEOQueueService()


@pytest.fixture
def crawl_job():
    """Create sample crawl job fixture."""
    return CrawlJob(
        url=HttpUrl("https://example.com"),
        data_source=DataSource.GOOGLE,
        status=CrawlStatus.PENDING,
        priority=50,
    )


async def test_enqueue_single_job(queue, crawl_job):
    """Test enqueueing single job."""
    result = await queue.enqueue_jobs(crawl_job)

    assert result.success
    assert result.output["queued_count"] == 1
    assert len(queue._queue) == 1


async def test_enqueue_multiple_jobs(queue, crawl_job):
    """Test enqueueing multiple jobs."""
    jobs = [crawl_job for _ in range(3)]
    result = await queue.enqueue_jobs(jobs)

    assert result.success
    assert result.output["queued_count"] == 3
    assert len(queue._queue) == 3


async def test_dequeue_batch(queue, crawl_job):
    """Test dequeuing batch of jobs."""
    jobs = [crawl_job for _ in range(5)]
    await queue.enqueue_jobs(jobs)

    batch = await queue.dequeue_batch(size=3)
    assert len(batch) == 3
    assert len(queue._queue) == 2


async def test_priority_ordering(queue):
    """Test jobs are ordered by priority."""
    jobs = [
        CrawlJob(
            url=HttpUrl("https://example.com"),
            data_source=DataSource.GOOGLE,
            priority=p,
        )
        for p in [10, 50, 30]
    ]
    await queue.enqueue_jobs(jobs)

    assert queue._queue[0].priority == 50  # Highest priority first
    assert queue._queue[-1].priority == 10  # Lowest priority last


async def test_queue_status(queue, crawl_job):
    """Test queue status reporting."""
    await queue.enqueue_jobs([crawl_job for _ in range(3)])

    status = queue.get_queue_status()
    assert status["queue_size"] == 3
    assert status["status_counts"][CrawlStatus.PENDING.value] == 3
    assert not status["is_processing"]
