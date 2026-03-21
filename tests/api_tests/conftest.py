"""
conftest.py — API Tests
Shared fixtures for API test suites.
"""
import pytest
from tests.api_tests.helpers.api_client import APIClient
from utils.config import settings


@pytest.fixture(scope="session")
def jsonplaceholder_client() -> APIClient:
    """Session-scoped client for JSONPlaceholder API."""
    return APIClient(base_url=settings.api.jsonplaceholder_url)


@pytest.fixture(scope="session")
def dummyjson_client() -> APIClient:
    """Session-scoped client for DummyJSON API (https://dummyjson.com)."""
    return APIClient(base_url=settings.api.dummyjson_url)
