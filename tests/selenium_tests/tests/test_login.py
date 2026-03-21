"""
Tests: Login — saucedemo.com
Covers: valid login, invalid credentials, locked user, empty fields, error dismissal.
"""
import json
import pytest
import allure
from pathlib import Path

from tests.selenium_tests.pages.login_page import LoginPage
from tests.selenium_tests.pages.inventory_page import InventoryPage

FIXTURES = json.loads(
    (Path(__file__).parent.parent / "fixtures" / "users.json").read_text()
)


@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:
    """
    Login test suite for Sauce Demo.
    Target: https://www.saucedemo.com/
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Navigate to login page before each test."""
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.login_page.load()

    # ------------------------------------------------------------------
    # Happy Path
    # ------------------------------------------------------------------

    @allure.title("TC_LOGIN_001 - Valid credentials redirect to inventory")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login_redirects_to_inventory(self):
        """Standard user can log in and lands on the inventory page."""
        user = FIXTURES["valid_users"]["standard"]

        with allure.step("Enter valid credentials and submit"):
            self.login_page.login(user["username"], user["password"])

        with allure.step("Assert user is on inventory page"):
            assert self.inventory_page.is_on_inventory_page(), (
                f"Expected inventory URL, got: {self.login_page.get_current_url()}"
            )
            assert self.inventory_page.get_page_title() == "Products"

    @allure.title("TC_LOGIN_002 - Page title is correct")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_title(self):
        """Login page has the expected browser title."""
        assert "Swag Labs" in self.login_page.get_title()

    @allure.title("TC_LOGIN_003 - Login button is present")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_button_is_present(self):
        """Login button renders on the page."""
        assert self.login_page.is_login_button_present()

    # ------------------------------------------------------------------
    # Negative / Error scenarios
    # ------------------------------------------------------------------

    @allure.title("TC_LOGIN_004 - Locked user sees error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_locked_user_shows_error(self):
        """A locked-out user cannot log in and sees the correct error."""
        user = FIXTURES["invalid_users"]["locked"]

        with allure.step("Attempt login with locked account"):
            self.login_page.login(user["username"], user["password"])

        with allure.step("Assert error message is shown"):
            assert self.login_page.is_error_displayed()
            assert user["expected_error"] in self.login_page.get_error_message()

    @allure.title("TC_LOGIN_005 - Wrong password shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_wrong_password_shows_error(self):
        """An incorrect password blocks access with a clear message."""
        user = FIXTURES["invalid_users"]["wrong_password"]

        with allure.step("Attempt login with wrong password"):
            self.login_page.login(user["username"], user["password"])

        with allure.step("Assert error message"):
            assert self.login_page.is_error_displayed()
            assert user["expected_error"] in self.login_page.get_error_message()

    @allure.title("TC_LOGIN_006 - Empty username shows validation error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_username_shows_validation(self):
        """Submitting without username shows a validation error."""
        user = FIXTURES["invalid_users"]["empty_username"]
        self.login_page.login(user["username"], user["password"])
        assert self.login_page.is_error_displayed()
        assert user["expected_error"] in self.login_page.get_error_message()

    @allure.title("TC_LOGIN_007 - Empty password shows validation error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_password_shows_validation(self):
        """Submitting without password shows a validation error."""
        user = FIXTURES["invalid_users"]["empty_password"]
        self.login_page.login(user["username"], user["password"])
        assert self.login_page.is_error_displayed()
        assert user["expected_error"] in self.login_page.get_error_message()

    @allure.title("TC_LOGIN_008 - Both fields empty shows validation error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_both_empty_shows_validation(self):
        """Submitting completely empty form shows a validation error."""
        user = FIXTURES["invalid_users"]["both_empty"]
        self.login_page.login(user["username"], user["password"])
        assert self.login_page.is_error_displayed()
        assert user["expected_error"] in self.login_page.get_error_message()

    @allure.title("TC_LOGIN_009 - Error banner can be dismissed")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.login
    def test_error_banner_can_be_dismissed(self):
        """Error message disappears after clicking the close button."""
        user = FIXTURES["invalid_users"]["locked"]
        self.login_page.login(user["username"], user["password"])

        assert self.login_page.is_error_displayed()

        with allure.step("Dismiss error banner"):
            self.login_page.close_error()

        assert not self.login_page.is_error_displayed()

    @allure.title("TC_LOGIN_010 - SQL injection does not bypass login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_sql_injection_does_not_bypass_login(self):
        """
        Security test: SQL injection payloads in credentials
        must not grant access.
        """
        malicious_inputs = [
            ("' OR '1'='1", "' OR '1'='1"),
            ("admin'--", "password"),
            ("'; DROP TABLE users; --", "anything"),
        ]
        for username, password in malicious_inputs:
            self.login_page.load()
            self.login_page.login(username, password)
            assert not self.inventory_page.is_on_inventory_page(), (
                f"SQL injection bypassed login with: {username}"
            )
