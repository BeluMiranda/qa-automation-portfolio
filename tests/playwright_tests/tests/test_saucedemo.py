"""
Tests: Login — Playwright (Python)
Same scenarios as Selenium suite — demonstrates multi-framework coverage.
"""
import re
import pytest
import allure
from playwright.sync_api import Page, expect

from tests.playwright_tests.pages.login_page import LoginPage
from tests.playwright_tests.pages.inventory_page import InventoryPage
from utils.config import settings


@allure.feature("Authentication")
@allure.story("Login - Playwright")
class TestLoginPlaywright:
    """
    Login tests using Playwright.
    These mirror the Selenium tests to demonstrate framework versatility.
    """

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.login_page.load()

    @allure.title("[PW] TC_LOGIN_001 - Valid login redirects to inventory")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.playwright
    def test_valid_login(self):
        """Standard user can log in successfully using Playwright."""
        self.login_page.login(
            settings.saucedemo.standard_user,
            settings.saucedemo.password,
        )
        expect(self.login_page.page).to_have_url(re.compile(r"inventory\.html"))
        assert self.inventory_page.get_page_title() == "Products"

    @allure.title("[PW] TC_LOGIN_002 - Locked user sees error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.playwright
    def test_locked_user(self):
        """Locked user is blocked with the correct error message."""
        self.login_page.login(settings.saucedemo.locked_user, settings.saucedemo.password)
        assert self.login_page.is_error_visible()
        assert "locked out" in self.login_page.get_error_message()

    @allure.title("[PW] TC_LOGIN_003 - Wrong password shows error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.playwright
    def test_wrong_password(self):
        """Wrong password shows the invalid credentials error."""
        self.login_page.login(settings.saucedemo.standard_user, "bad_password")
        assert self.login_page.is_error_visible()
        assert "do not match" in self.login_page.get_error_message()

    @allure.title("[PW] TC_LOGIN_004 - Empty fields show validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.playwright
    def test_empty_fields(self):
        """Submitting empty fields shows a validation message."""
        self.login_page.login("", "")
        assert self.login_page.is_error_visible()
        assert "Username is required" in self.login_page.get_error_message()

    @allure.title("[PW] TC_LOGIN_005 - Error is dismissible")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.playwright
    def test_error_can_be_dismissed(self):
        """Error banner can be closed via the X button."""
        self.login_page.login(settings.saucedemo.locked_user, settings.saucedemo.password)
        assert self.login_page.is_error_visible()
        self.login_page.close_error()
        assert not self.login_page.is_error_visible()


@allure.feature("Inventory")
@allure.story("Inventory - Playwright")
class TestInventoryPlaywright:
    """
    Inventory tests using Playwright.
    Demonstrates Playwright-specific features like auto-waiting.
    """

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.inventory = InventoryPage(authenticated_page)

    @allure.title("[PW] TC_INV_001 - Inventory loads with 6 products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.playwright
    def test_inventory_loads(self):
        """Inventory page loads correctly after authentication."""
        assert self.inventory.is_on_page()
        assert self.inventory.get_page_title() == "Products"
        assert len(self.inventory.get_product_names()) == 6

    @allure.title("[PW] TC_INV_002 - Sort A→Z works")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.playwright
    def test_sort_a_to_z(self):
        """Products are correctly sorted A to Z."""
        self.inventory.sort_by("az")
        names = self.inventory.get_product_names()
        assert names == sorted(names)

    @allure.title("[PW] TC_INV_003 - Add item to cart updates badge")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.playwright
    def test_add_item_updates_badge(self):
        """Adding a product updates the cart badge counter."""
        self.inventory.add_to_cart(0)
        assert self.inventory.get_cart_count() == 1
