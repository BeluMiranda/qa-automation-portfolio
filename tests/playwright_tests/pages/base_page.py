"""
Page: BasePage (Playwright)
Thin wrapper over Playwright's Page object — consistent interface with Selenium POM.
"""
import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """
    Base page for Playwright POM.
    Wraps common interactions so subclasses stay readable.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    # ------------------------------------------------------------------
    # Interaction helpers
    # ------------------------------------------------------------------

    def fill(self, selector: str, text: str) -> None:
        self.page.fill(selector, text)

    def click(self, selector: str) -> None:
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def wait_for_url(self, url_pattern: str) -> None:
        self.page.wait_for_url(url_pattern)

    def screenshot(self, name: str = "screenshot") -> None:
        """Take screenshot and attach to Allure."""
        screenshot_bytes = self.page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
