"""
Helper: APIClient
Base HTTP client used by all API test suites.
Wraps requests with logging, retries, and assertion helpers.
"""
import time
from typing import Any, Optional

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """
    Reusable API client with:
    - Automatic retries on transient errors (429, 500, 502, 503, 504)
    - Request/response logging
    - Response assertion helpers
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._build_session()

    # ------------------------------------------------------------------
    # Session setup
    # ------------------------------------------------------------------

    def _build_session(self) -> Session:
        session = Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        return session

    # ------------------------------------------------------------------
    # HTTP Methods
    # ------------------------------------------------------------------

    def get(self, endpoint: str, params: Optional[dict] = None, **kwargs) -> Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json: Optional[dict] = None, **kwargs) -> Response:
        return self._request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: Optional[dict] = None, **kwargs) -> Response:
        return self._request("PUT", endpoint, json=json, **kwargs)

    def patch(self, endpoint: str, json: Optional[dict] = None, **kwargs) -> Response:
        return self._request("PATCH", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self._request("DELETE", endpoint, **kwargs)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start = time.monotonic()

        logger.info("API Request", extra={"method": method, "url": url})

        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs,
        )

        elapsed_ms = round((time.monotonic() - start) * 1000)
        logger.info(
            "API Response",
            extra={
                "method": method,
                "url": url,
                "status": response.status_code,
                "elapsed_ms": elapsed_ms,
            },
        )
        return response

    # ------------------------------------------------------------------
    # Assertion helpers — keep tests clean
    # ------------------------------------------------------------------

    def assert_status(self, response: Response, expected: int) -> None:
        """Assert HTTP status code with a descriptive message."""
        assert response.status_code == expected, (
            f"Expected {expected}, got {response.status_code}. "
            f"Body: {response.text[:500]}"
        )

    def assert_json_key(self, response: Response, key: str) -> None:
        """Assert a key exists in the JSON response body."""
        body = response.json()
        assert key in body, f"Key '{key}' not found in response: {body}"

    def assert_json_value(self, response: Response, key: str, expected: Any) -> None:
        """Assert a JSON key has the expected value."""
        body = response.json()
        assert body.get(key) == expected, (
            f"Expected '{key}' = {expected!r}, got {body.get(key)!r}"
        )

    def assert_response_time(self, response: Response, max_ms: int) -> None:
        """Assert the response was received within max_ms milliseconds."""
        elapsed = response.elapsed.total_seconds() * 1000
        assert elapsed <= max_ms, (
            f"Response took {elapsed:.0f}ms, expected <= {max_ms}ms"
        )
