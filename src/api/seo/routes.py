from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from src.api.seo.dependencies import get_analytics_service
from src.api.seo.models import InsightsResponse, MetricsResponse, TrendResponse
from src.services.seo.analytics import SEOAnalyticsService

router = APIRouter(prefix="/seo", tags=["seo"])


@router.get("/sites/{site_id}/metrics", response_model=MetricsResponse)
async def get_metrics(
    site_id: str,
    analytics_service: SEOAnalyticsService = Depends(get_analytics_service),
):
    """Get site metrics."""
    metrics = await analytics_service.analyze_metrics(site_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Site metrics not found")

    return MetricsResponse(
        site_id=site_id,
        metrics=metrics,
        timestamp=datetime.utcnow()
    )


@router.get("/sites/{site_id}/insights", response_model=InsightsResponse)
async def get_insights(
    site_id: str,
    analytics_service: SEOAnalyticsService = Depends(get_analytics_service),
):
    """Get site insights and recommendations."""
    insights, recommendations = await analytics_service.generate_insights(site_id)
    if not insights and not recommendations:
        raise HTTPException(status_code=404, detail="Site insights not found")

    return InsightsResponse(
        site_id=site_id,
        insights=insights,
        recommendations=recommendations
    )


@router.get("/sites/{site_id}/trends", response_model=TrendResponse)
async def get_trends(
    site_id: str,
    days: int = 30,
    analytics_service: SEOAnalyticsService = Depends(get_analytics_service),
):
    """Get site metrics trends."""
    trends = await analytics_service.compute_trends(site_id, days)
    if not trends:
        raise HTTPException(status_code=404, detail="Site trends not found")

    return TrendResponse(
        site_id=site_id,
        trends=trends,
        period_days=days
    )
