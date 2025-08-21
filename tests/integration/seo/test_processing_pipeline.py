"""Integration tests for SEO processing pipeline."""


import pytest
from pydantic import HttpUrl

from src.models.seo import CrawlJob, CrawlStatus, DataSource, SEOMetrics
from src.services.seo.processor import SEOProcessorService
from src.services.seo.queue import SEOQueueService
from src.services.seo.storage import SEOStorageService


@pytest.fixture
def queue():
    """Create queue service fixture."""
    return SEOQueueService()


@pytest.fixture
def processor():
    """Create processor service fixture."""
    return SEOProcessorService()


@pytest.fixture
def storage():
    """Create storage service fixture."""
    return SEOStorageService()


@pytest.fixture
def crawl_job():
    """Create sample crawl job fixture."""
    return CrawlJob(
        url=HttpUrl("https://example.com"),
        data_source=DataSource.GOOGLE,
        status=CrawlStatus.PENDING,
        priority=50,
    )


async def test_end_to_end_processing(queue, processor, storage, crawl_job):
    """Test complete processing pipeline."""
    # 1. Enqueue jobs
    jobs = [crawl_job for _ in range(3)]
    enqueue_result = await queue.enqueue_jobs(jobs)
    assert enqueue_result.success

    # 2. Process jobs
    batch = await queue.dequeue_batch()
    process_result = await processor.process_jobs(batch)
    assert process_result.success

    processed_metrics = process_result.output["processed_metrics"]
    assert len(processed_metrics) == 3

    # 3. Store results
    store_result = await storage.store_metrics(processed_metrics)
    assert store_result.success

    # 4. Query stored results
    query_result = await storage.query_metrics(
        url=str(crawl_job.url),
        min_authority=0.0,
        min_visibility=0.0,
    )
    assert query_result.success

    queried_metrics = query_result.output["metrics"]
    assert len(queried_metrics) > 0
    assert all(isinstance(m, SEOMetrics) for m in queried_metrics)


async def test_pipeline_error_handling(queue, processor, storage, crawl_job):
    """Test pipeline error handling and recovery."""
    # 1. Create job with invalid URL
    bad_job = CrawlJob(
        url=HttpUrl("https://invalid-domain-that-doesnt-exist.com"),
        data_source=DataSource.GOOGLE,
        status=CrawlStatus.PENDING,
        priority=50,
    )

    # 2. Process invalid job
    process_result = await processor.process_jobs([bad_job])
    assert not process_result.success
    assert len(process_result.errors) > 0

    # 3. Verify job status is updated
    assert bad_job.status == CrawlStatus.FAILED
    assert bad_job.error_message is not None


async def test_concurrent_processing(queue, processor, storage, crawl_job):
    """Test concurrent job processing."""
    # 1. Enqueue multiple jobs
    jobs = [crawl_job for _ in range(10)]
    await queue.enqueue_jobs(jobs)

    # 2. Process jobs in parallel batches
    batches = []
    while len(queue._queue) > 0:
        batch = await queue.dequeue_batch(size=3)
        batches.append(batch)

    results = await processor.process_jobs(jobs)
    assert results.success
    assert "processed_metrics" in results.output
