"""FastAPI dependencies for SEO endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.services.seo.analytics import SEOAnalyticsService
from src.services.seo.processor import SEOProcessorService


async def get_analytics_service() -> SEOAnalyticsService:
    """Dependency for analytics service."""
    return SEOAnalyticsService()


async def get_processor_service() -> SEOProcessorService:
    """Dependency for processor service."""
    return SEOProcessorService()


# Type annotations for dependencies
AnalyticsService = Annotated[SEOAnalyticsService, Depends(get_analytics_service)]
ProcessorService = Annotated[SEOProcessorService, Depends(get_processor_service)]
