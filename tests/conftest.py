"""Test configuration and fixtures."""

import os
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest

os.environ["API_CORS_ORIGINS"] = "[]"  # Empty list for tests
os.environ["API_KEY"] = "test-key"  # Test API key