"""
Tests: Inventory — saucedemo.com/inventory.html
Covers: product listing, sorting, add/remove from cart.
"""
import pytest
import allure

from tests.selenium_tests.pages.login_page import LoginPage
from tests.selenium_tests.pages.inventory_page import InventoryPage
from utils.config import settings


@allure.feature("Inventory")
@allure.story("Product Listing & Sorting")
class TestInventory:
    """
    Inventory page test suite.
    Requires a successful login before each test.
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Log in as standard user before each test."""
        login = LoginPage(driver)
        login.load()
        login.login(settings.saucedemo.standard_user, settings.saucedemo.password)
        self.inventory = InventoryPage(driver)

    # ------------------------------------------------------------------
    # Display tests
    # ------------------------------------------------------------------

    @allure.title("TC_INV_001 - Inventory page loads with correct title")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_inventory_page_loads(self):
        """Products page displays with 'Products' header."""
        assert self.inventory.is_on_inventory_page()
        assert self.inventory.get_page_title() == "Products"

    @allure.title("TC_INV_002 - Six products are displayed")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_six_products_are_displayed(self):
        """Sauce Demo has exactly 6 products on the inventory page."""
        assert self.inventory.get_product_count() == 6

    @allure.title("TC_INV_003 - All product names are non-empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_all_product_names_are_non_empty(self):
        """Every product has a visible non-empty name."""
        names = self.inventory.get_product_names()
        for name in names:
            assert name.strip() != "", f"Found empty product name: '{name}'"

    @allure.title("TC_INV_004 - All product prices are positive numbers")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_all_product_prices_are_positive(self):
        """Every product has a price greater than zero."""
        prices = self.inventory.get_product_prices()
        for price in prices:
            assert price > 0, f"Non-positive price found: {price}"

    # ------------------------------------------------------------------
    # Sorting tests
    # ------------------------------------------------------------------

    @allure.title("TC_INV_005 - Sort A to Z")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_a_to_z(self):
        """Products can be sorted alphabetically A → Z."""
        self.inventory.sort_by("az")
        names = self.inventory.get_product_names()
        assert names == sorted(names), "Products are not sorted A→Z"

    @allure.title("TC_INV_006 - Sort Z to A")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_z_to_a(self):
        """Products can be sorted alphabetically Z → A."""
        self.inventory.sort_by("za")
        names = self.inventory.get_product_names()
        assert names == sorted(names, reverse=True), "Products are not sorted Z→A"

    @allure.title("TC_INV_007 - Sort price Low to High")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_price_low_to_high(self):
        """Products can be sorted by price ascending."""
        self.inventory.sort_by("lohi")
        prices = self.inventory.get_product_prices()
        assert prices == sorted(prices), "Prices are not sorted Low→High"

    @allure.title("TC_INV_008 - Sort price High to Low")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_price_high_to_low(self):
        """Products can be sorted by price descending."""
        self.inventory.sort_by("hilo")
        prices = self.inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True), "Prices are not sorted High→Low"

    # ------------------------------------------------------------------
    # Cart tests
    # ------------------------------------------------------------------

    @allure.title("TC_INV_009 - Add one item updates cart badge")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_one_item_updates_cart_badge(self):
        """Cart badge shows '1' after adding one product."""
        self.inventory.add_item_to_cart(0)
        assert self.inventory.get_cart_item_count() == 1

    @allure.title("TC_INV_010 - Add multiple items updates cart count")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_items_updates_cart_count(self):
        """Cart count updates correctly when adding multiple items."""
        self.inventory.add_item_to_cart(0)
        self.inventory.add_item_to_cart(1)
        self.inventory.add_item_to_cart(2)
        assert self.inventory.get_cart_item_count() == 3

    @allure.title("TC_INV_011 - Remove item decreases cart count")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_item_decreases_cart_count(self):
        """Removing a product from cart decreases the badge count."""
        self.inventory.add_item_to_cart(0)
        self.inventory.add_item_to_cart(1)
        assert self.inventory.get_cart_item_count() == 2

        self.inventory.remove_item_from_cart(0)
        assert self.inventory.get_cart_item_count() == 1

    @allure.title("TC_INV_012 - Cart badge hidden when cart is empty")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_no_badge_when_cart_empty(self):
        """No cart badge is displayed when no items have been added."""
        assert self.inventory.get_cart_item_count() == 0
