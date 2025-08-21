"""SEO data processing service."""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from datetime import UTC, datetime

from src.config.settings import settings
from src.models import ExecutionResult
from src.models.seo import CrawlJob, CrawlStatus, SEOMetrics
from src.services.seo.collector import SEOCollectorService


class SEOProcessorService:
    """Service for processing and normalizing SEO data."""

    def __init__(self) -> None:
        """Initialize the processor service."""
        self.collector = SEOCollectorService()
        self.batch_size = settings.seo.batch_size
        self.min_score = settings.seo.min_score_threshold
        self.max_score = settings.seo.max_score_threshold

    async def process_jobs(self, jobs: Sequence[CrawlJob]) -> ExecutionResult:
        """
        Process a batch of crawl jobs with normalization.

        Args:
            jobs: Sequence of crawl jobs to process

        Returns:
            ExecutionResult containing processed metrics or errors
        """
        start_time = datetime.now(UTC)
        results = []
        errors = []

        # Process in batches for memory efficiency
        for i in range(0, len(jobs), self.batch_size):
            batch = jobs[i : i + self.batch_size]
            batch_results = await asyncio.gather(
                *[self._process_job(job) for job in batch],
                return_exceptions=True
            )

            for result in batch_results:
                if isinstance(result, Exception):
                    errors.append(str(result))
                elif result:  # Skip None results
                    results.append(result)

        end_time = datetime.now(UTC)
        execution_time = (end_time - start_time).total_seconds()

        # Consider processing failed if any job had errors or no metrics were processed
        if errors or not results:
            return ExecutionResult(
                success=False,
                errors=errors or ["No metrics were successfully processed"],
                output={"processed_metrics": results},
                performance_metrics={
                    "execution_time": execution_time,
                    "processed_count": len(results),
                    "error_count": len(errors),
                },
                execution_time=execution_time,
            )
        
        return ExecutionResult(
            success=True,
            output={"processed_metrics": results},
            performance_metrics={
                "execution_time": execution_time,
                "processed_count": len(results),
            },
            execution_time=execution_time,
        )

    async def _process_job(self, job: CrawlJob) -> SEOMetrics | None:
        """
        Process a single crawl job with data normalization.

        Args:
            job: Crawl job to process

        Returns:
            Normalized SEO metrics or None if processing failed
        """
        try:
            # Collect raw metrics
            result = await self.collector.collect_metrics(job)
            if not result.success or not result.output:
                job.status = CrawlStatus.FAILED
                job.error_message = (
                    result.errors[0] if result.errors else "Unknown collection error"
                )
                job.updated_at = datetime.now(UTC)
                return None

            metrics = SEOMetrics(**result.output["metrics"])
            
            # Normalize metrics
            normalized = await self._normalize_metrics(metrics)
            
            # Update job status
            job.metrics = normalized
            job.status = CrawlStatus.COMPLETED
            job.updated_at = datetime.now(UTC)
            
            return normalized

        except Exception as e:
            job.status = CrawlStatus.FAILED
            job.error_message = str(e)
            job.updated_at = datetime.now(UTC)
            return None

    async def _normalize_metrics(self, metrics: SEOMetrics) -> SEOMetrics:
        """
        Normalize SEO metrics within defined thresholds.

        Args:
            metrics: Raw SEO metrics to normalize

        Returns:
            Normalized SEO metrics
        """
        try:
            # Normalize visibility score
            metrics.visibility_score = max(
                self.min_score,
                min(metrics.visibility_score, self.max_score)
            )
            
            # Normalize page authority
            metrics.page_authority = max(
                self.min_score,
                min(metrics.page_authority, self.max_score)
            )
            
            # Ensure non-negative values
            metrics.backlinks_count = max(0, metrics.backlinks_count)
            metrics.organic_traffic = max(0, metrics.organic_traffic)
            
            # Normalize keyword rankings (ensure positive ranks)
            metrics.keyword_rankings = {
                k: max(1, v) for k, v in metrics.keyword_rankings.items()
            }
            
            # Update last processed timestamp
            metrics.last_updated = datetime.now(UTC)
            
            return metrics

        except Exception as e:
            raise ValueError(f"Failed to normalize metrics: {str(e)}") from e