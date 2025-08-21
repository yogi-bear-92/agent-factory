"""SEO data storage service."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from src.config.settings import settings
from src.knowledge.vector_store.chroma_client import ChromaVectorStore
from src.models import ExecutionResult, KnowledgeEntry, SourceType
from src.models.seo import SEOMetrics


class SEOStorageService:
    """Service for storing and retrieving SEO data."""

    def __init__(self) -> None:
        """Initialize the storage service."""
        self.vector_store = ChromaVectorStore()
        self.collection_name = "seo_metrics"
        self.cache_ttl = settings.seo.cache_ttl

    async def store_metrics(
        self, metrics: SEOMetrics | Sequence[SEOMetrics]
    ) -> ExecutionResult:
        """
        Store SEO metrics in vector store.

        Args:
            metrics: Single or sequence of SEO metrics to store

        Returns:
            ExecutionResult indicating storage success/failure
        """
        start_time = datetime.now(UTC)

        try:
            # Convert single metric to sequence
            metrics_seq = [metrics] if isinstance(metrics, SEOMetrics) else metrics

            # Store each metric as a knowledge entry
            stored_ids = []
            for metric in metrics_seq:
                doc_id = f"seo_{metric.url.host}_{metric.last_updated.timestamp()}"
                metadata = {
                    "url": str(metric.url),
                    "timestamp": metric.last_updated.isoformat(),
                    "page_authority": metric.page_authority,
                    "visibility_score": metric.visibility_score,
                }

                entry = KnowledgeEntry(
                    id=doc_id,
                    content=metric.model_dump_json(),
                    metadata=metadata,
                    source_type=SourceType.SEO,
                    tags=["seo", "metrics"],
                )
                stored_id = await self.vector_store.store_knowledge(entry)
                stored_ids.append(stored_id)

            end_time = datetime.now(UTC)
            execution_time = (end_time - start_time).total_seconds()

            return ExecutionResult(
                success=True,
                output={"stored_count": len(stored_ids)},
                performance_metrics={
                    "execution_time": execution_time,
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

    async def query_metrics(
        self,
        url: str | None = None,
        min_authority: float | None = None,
        min_visibility: float | None = None,
        limit: int = 10,
    ) -> ExecutionResult:
        """
        Query stored SEO metrics with filtering.

        Args:
            url: Optional URL to filter by
            min_authority: Minimum page authority score
            min_visibility: Minimum visibility score
            limit: Maximum number of results

        Returns:
            ExecutionResult containing matching metrics
        """
        start_time = datetime.now(UTC)

        try:
            # Build query
            query_filters = []
            if url:
                query_filters.append(f"URL: {url}")
            if min_authority is not None:
                query_filters.append(f"Authority >= {min_authority}")
            if min_visibility is not None:
                query_filters.append(f"Visibility >= {min_visibility}")

            query = " AND ".join(query_filters) if query_filters else ""

            # Query vector store
            entries = await self.vector_store.query_similar(
                query=query,
                n_results=limit,
                source_type=SourceType.SEO,
            )

            # Parse results back to SEOMetrics
            metrics = []
            for entry in entries:
                try:
                    # Filter results based on criteria
                    if min_authority is not None and entry.metadata.get("page_authority", 0) < min_authority:
                        continue
                    if min_visibility is not None and entry.metadata.get("visibility_score", 0) < min_visibility:
                        continue

                    metric = SEOMetrics.model_validate_json(entry.content)
                    metrics.append(metric)
                except Exception:
                    continue

            end_time = datetime.now(UTC)
            execution_time = (end_time - start_time).total_seconds()

            return ExecutionResult(
                success=True,
                output={"metrics": metrics},
                performance_metrics={
                    "execution_time": execution_time,
                    "result_count": len(metrics),
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
