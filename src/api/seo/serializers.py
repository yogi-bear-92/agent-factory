"""SEO API serialization utilities."""

from __future__ import annotations

from typing import Any

from pydantic import HttpUrl


class SEOJSONEncoder:
    """Custom JSON encoder for SEO types."""

    @staticmethod
    def default(obj: Any) -> Any:
        """Convert object to JSON serializable format."""
        if isinstance(obj, HttpUrl):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
