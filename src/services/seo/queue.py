"""SEO job queue management service."""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from src.config.settings import settings
from src.models import ExecutionResult
from src.models.seo import CrawlJob, CrawlStatus


class SEOQueueService:
    """Service for managing SEO processing job queue."""

    def __init__(self) -> None:
        """Initialize the queue service."""
        self.processing_interval = settings.seo.processing_interval
        self.batch_size = settings.seo.batch_size
        self._queue: list[CrawlJob] = []
        self._processing = False

    async def enqueue_jobs(self, jobs: CrawlJob | Sequence[CrawlJob]) -> ExecutionResult:
        """
        Add jobs to processing queue.

        Args:
            jobs: Single job or sequence of jobs to enqueue

        Returns:
            ExecutionResult indicating enqueue success/failure
        """
        start_time = datetime.now(UTC)

        try:
            # Convert single job to sequence
            job_seq = [jobs] if isinstance(jobs, CrawlJob) else jobs

            # Update job timestamps
            current_time = datetime.now(UTC)
            for job in job_seq:
                job.created_at = current_time
                job.updated_at = current_time
                job.status = CrawlStatus.PENDING

            # Add to queue sorted by priority
            self._queue.extend(job_seq)
            self._queue.sort(key=lambda x: (-x.priority, x.created_at))

            end_time = datetime.now(UTC)
            execution_time = (end_time - start_time).total_seconds()

            return ExecutionResult(
                success=True,
                output={"queued_count": len(job_seq)},
                performance_metrics={
                    "execution_time": execution_time,
                    "queue_size": len(self._queue),
                },
                execution_time=execution_time,
            )

        except Exception as e:
            end_time = datetime.now(UTC)
            execution_time = (end_time - start_time).total_seconds()

            return ExecutionResult(
                success=False,
                errors=[str(e)],
                performance_metrics={
                    "execution_time": execution_time,
                },
                execution_time=execution_time,
            )

    async def dequeue_batch(self, size: int | None = None) -> Sequence[CrawlJob]:
        """
        Get next batch of jobs for processing.

        Args:
            size: Optional batch size override

        Returns:
            Sequence of jobs to process
        """
        batch_size = size or self.batch_size
        if not self._queue:
            return []

        batch = self._queue[:batch_size]
        self._queue = self._queue[batch_size:]
        return batch

    async def start_processing(self) -> None:
        """Start the job processing loop."""
        self._processing = True
        while self._processing:
            if self._queue:
                batch = await self.dequeue_batch()
                for job in batch:
                    job.status = CrawlStatus.IN_PROGRESS
                    job.updated_at = datetime.now(UTC)
            await asyncio.sleep(self.processing_interval)

    async def stop_processing(self) -> None:
        """Stop the job processing loop."""
        self._processing = False

    def get_queue_status(self) -> dict[str, Any]:
        """
        Get current queue status.

        Returns:
            Dict containing queue metrics
        """
        status_counts: dict[str, int] = {
            status.value: 0 for status in CrawlStatus
        }

        for job in self._queue:
            status_counts[job.status.value] += 1

        return {
            "queue_size": len(self._queue),
            "status_counts": status_counts,
            "is_processing": self._processing,
        }
