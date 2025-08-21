"""SEO-specific settings."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SEOSettings(BaseModel):
    """SEO configuration settings."""

    batch_size: int = Field(default=10, ge=1)
    min_score_threshold: float = Field(default=0.0, ge=0.0, le=100.0)
    max_score_threshold: float = Field(default=100.0, ge=0.0, le=100.0)
    trend_window_days: int = Field(default=30, ge=1)
    significance_threshold: float = Field(default=10.0, ge=0.0)