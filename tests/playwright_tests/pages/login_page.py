"""
Page: LoginPage (Playwright) — saucedemo.com
"""
from playwright.sync_api import Page, expect

from tests.playwright_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Represents the Login page using Playwright.
    Mirrors the Selenium LoginPage interface for comparison.
    """

    _USERNAME = "[data-test='username']"
    _PASSWORD = "[data-test='password']"
    _LOGIN_BTN = "[data-test='login-button']"
    _ERROR_MSG = "[data-test='error']"
    _ERROR_CLOSE = ".error-button"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def load(self) -> "LoginPage":
        self.navigate("https://www.saucedemo.com/")
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self._USERNAME, username)
        self.fill(self._PASSWORD, password)
        self.click(self._LOGIN_BTN)

    def close_error(self) -> None:
        self.click(self._ERROR_CLOSE)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def is_error_visible(self) -> bool:
        return self.is_visible(self._ERROR_MSG)
