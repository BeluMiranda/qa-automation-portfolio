"""
conftest.py — Playwright Tests
Fixtures for the Playwright test suite.
Uses pytest-playwright for browser/page lifecycle management.
"""
import pytest
from playwright.sync_api import Page, BrowserContext, Browser

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override context defaults: viewport, locale, timezone."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "record_video_dir": None,  # set to "videos/" if you want recordings
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Pass launch options (headless, slow_mo) to the browser."""
    return {
        **browser_type_launch_args,
        "headless": settings.browser.headless,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    }


@pytest.fixture()
def authenticated_page(page: Page) -> Page:
    """
    Returns a Page already logged in to Sauce Demo.
    Use this in tests that require authentication.
    """
    page.goto(settings.saucedemo.url)
    page.fill("[data-test='username']", settings.saucedemo.standard_user)
    page.fill("[data-test='password']", settings.saucedemo.password)
    page.click("[data-test='login-button']")
    page.wait_for_url("**/inventory.html")
    logger.info("Playwright: authenticated page ready")
    return page
