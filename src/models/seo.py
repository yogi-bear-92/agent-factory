from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class CrawlStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"


class DataSource(str, Enum):
    GOOGLE = "google"
    SEMRUSH = "semrush"
    AHREFS = "ahrefs"


class CrawlJob(BaseModel):
    site_id: str
    url: HttpUrl
    status: CrawlStatus = CrawlStatus.PENDING
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    error: str | None = None


class SEOMetrics(BaseModel):
    site_id: str
    visibility: float = 0.0
    traffic: int = 0
    backlinks: int = 0
    keywords: int = 0
    source: DataSource
    created_at: datetime


class SiteMetrics(BaseModel):
    site_id: str
    url: HttpUrl
    title: str
    description: str | None = None
    keywords: list[str] = []
    
    # SEO Metrics
    visibility_score: float = 0.0
    performance_score: float = 0.0
    optimization_score: float = 0.0
    
    # Meta Information
    created_at: datetime
    updated_at: datetime