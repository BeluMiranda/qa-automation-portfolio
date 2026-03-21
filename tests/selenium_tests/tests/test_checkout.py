"""
Tests: Checkout — saucedemo.com
Covers: full checkout flow, validation errors, cancel navigation.
"""
import json
import pytest
import allure
from pathlib import Path

from tests.selenium_tests.pages.login_page import LoginPage
from tests.selenium_tests.pages.inventory_page import InventoryPage
from tests.selenium_tests.pages.cart_page import (
    CartPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from utils.config import settings

FIXTURES = json.loads(
    (Path(__file__).parent.parent / "fixtures" / "users.json").read_text()
)


@allure.feature("Checkout")
@allure.story("Purchase Flow")
class TestCheckout:
    """
    End-to-end checkout test suite.
    Requires login + at least one item in cart before each test.
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Pre-condition: user is logged in with one item in cart.
        """
        login = LoginPage(driver)
        login.load()
        login.login(settings.saucedemo.standard_user, settings.saucedemo.password)

        self.inventory = InventoryPage(driver)
        self.inventory.add_item_to_cart(0)
        self.inventory.go_to_cart()

        self.cart = CartPage(driver)
        self.checkout_one = CheckoutStepOnePage(driver)
        self.checkout_two = CheckoutStepTwoPage(driver)
        self.checkout_complete = CheckoutCompletePage(driver)

    # ------------------------------------------------------------------
    # Cart page
    # ------------------------------------------------------------------

    @allure.title("TC_CART_001 - Cart shows added item")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_shows_added_item(self):
        """Cart page displays the item that was added from inventory."""
        assert self.cart.get_item_count() == 1

    @allure.title("TC_CART_002 - Removing item from cart empties it")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_item_from_cart(self):
        """An item removed from the cart page disappears from the list."""
        self.cart.remove_item(0)
        assert self.cart.is_cart_empty()

    # ------------------------------------------------------------------
    # Checkout Step 1 — Customer Info
    # ------------------------------------------------------------------

    @allure.title("TC_CHKOUT_001 - Checkout: missing first name shows error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_missing_first_name(self):
        """Omitting first name on checkout info shows a validation error."""
        data = FIXTURES["checkout_data"]["missing_firstname"]
        self.cart.proceed_to_checkout()
        self.checkout_one.fill_customer_info(data["first_name"], data["last_name"], data["postal_code"])
        self.checkout_one.click_continue()
        assert self.checkout_one.has_error()
        assert data["expected_error"] in self.checkout_one.get_error()

    @allure.title("TC_CHKOUT_002 - Checkout: missing last name shows error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_missing_last_name(self):
        """Omitting last name on checkout info shows a validation error."""
        data = FIXTURES["checkout_data"]["missing_lastname"]
        self.cart.proceed_to_checkout()
        self.checkout_one.fill_customer_info(data["first_name"], data["last_name"], data["postal_code"])
        self.checkout_one.click_continue()
        assert self.checkout_one.has_error()
        assert data["expected_error"] in self.checkout_one.get_error()

    @allure.title("TC_CHKOUT_003 - Checkout: missing postal code shows error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_missing_postal_code(self):
        """Omitting postal code on checkout info shows a validation error."""
        data = FIXTURES["checkout_data"]["missing_postal"]
        self.cart.proceed_to_checkout()
        self.checkout_one.fill_customer_info(data["first_name"], data["last_name"], data["postal_code"])
        self.checkout_one.click_continue()
        assert self.checkout_one.has_error()
        assert data["expected_error"] in self.checkout_one.get_error()

    # ------------------------------------------------------------------
    # Full E2E Flow
    # ------------------------------------------------------------------

    @allure.title("TC_CHKOUT_004 - Complete purchase end-to-end")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_complete_purchase_end_to_end(self):
        """
        End-to-end happy path: add item → cart → checkout info
        → review summary → finish → order confirmed.
        """
        checkout_data = FIXTURES["checkout_data"]["valid"]

        with allure.step("Proceed to checkout"):
            self.cart.proceed_to_checkout()

        with allure.step("Fill customer information"):
            self.checkout_one.fill_customer_info(
                checkout_data["first_name"],
                checkout_data["last_name"],
                checkout_data["postal_code"],
            )
            self.checkout_one.click_continue()

        with allure.step("Review order summary"):
            assert self.checkout_two.get_item_count() == 1
            assert "$" in self.checkout_two.get_total()

        with allure.step("Finish order"):
            self.checkout_two.click_finish()

        with allure.step("Assert order confirmation"):
            assert self.checkout_complete.is_order_complete()

    @allure.title("TC_CHKOUT_005 - Cancel from checkout returns to inventory")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_cancel_checkout_returns_to_inventory(self):
        """Clicking Cancel on step 1 returns the user to the cart page."""
        self.cart.proceed_to_checkout()
        self.checkout_one.click_cancel()
        assert self.cart.is_cart_page()

    @allure.title("TC_CHKOUT_006 - Back to products after order completion")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_back_to_products_after_completion(self):
        """Back button on completion page returns to inventory."""
        checkout_data = FIXTURES["checkout_data"]["valid"]
        self.cart.proceed_to_checkout()
        self.checkout_one.fill_customer_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"],
        )
        self.checkout_one.click_continue()
        self.checkout_two.click_finish()
        self.checkout_complete.back_to_home()
        assert self.inventory.is_on_inventory_page()
