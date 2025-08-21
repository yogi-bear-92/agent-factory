from datetime import datetime

from pydantic import BaseModel


class MetricsResponse(BaseModel):
    site_id: str
    metrics: dict[str, float]
    timestamp: datetime


class InsightsResponse(BaseModel):
    site_id: str
    insights: list[str]
    recommendations: list[str]


class TrendResponse(BaseModel):
    site_id: str
    trends: list[dict[str, float]]
    period_days: int
