"""
Page: LoginPage — saucedemo.com
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.selenium_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Represents the Login page of Sauce Demo.
    URL: https://www.saucedemo.com/
    """

    # ------------------------------------------------------------------
    # Locators (centralised — only change here if UI changes)
    # ------------------------------------------------------------------
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")
    _ERROR_CLOSE = (By.CLASS_NAME, "error-button")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def load(self) -> "LoginPage":
        """Navigate to login page. Returns self for chaining."""
        self.open("https://www.saucedemo.com/")
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.type_text(self._USERNAME, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(self._PASSWORD, password)
        return self

    def click_login(self) -> None:
        self.click(self._LOGIN_BTN)

    def login(self, username: str, password: str) -> None:
        """Full login flow in one call."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def close_error(self) -> "LoginPage":
        """Dismiss the error banner."""
        self.click(self._ERROR_CLOSE)
        return self

    # ------------------------------------------------------------------
    # Getters / Assertions helpers
    # ------------------------------------------------------------------

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def is_error_displayed(self) -> bool:
        return self.is_element_visible(self._ERROR_MSG)

    def is_login_button_present(self) -> bool:
        return self.is_element_present(self._LOGIN_BTN)
