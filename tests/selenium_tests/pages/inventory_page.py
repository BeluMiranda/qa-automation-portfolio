"""
Page: InventoryPage — saucedemo.com/inventory.html
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from tests.selenium_tests.pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Represents the Inventory (products) page.
    URL: https://www.saucedemo.com/inventory.html
    """

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    _ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _REMOVE_BTNS = (By.CSS_SELECTOR, "[data-test^='remove']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    _BURGER_MENU = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def sort_by(self, option: str) -> "InventoryPage":
        """
        Sort products.
        Options: 'az' | 'za' | 'lohi' | 'hilo'
        """
        select = Select(self.find_visible_element(self._SORT_DROPDOWN))
        select.select_by_value(option)
        return self

    def add_item_to_cart(self, index: int = 0) -> "InventoryPage":
        """Add item by index (0-based) to cart."""
        buttons = self.driver.find_elements(*self._ADD_TO_CART_BTNS)
        buttons[index].click()
        return self

    def add_all_items_to_cart(self) -> "InventoryPage":
        """Add all available items to cart."""
        buttons = self.driver.find_elements(*self._ADD_TO_CART_BTNS)
        for btn in buttons:
            btn.click()
        return self

    def remove_item_from_cart(self, index: int = 0) -> "InventoryPage":
        """Remove item by index (0-based) from cart."""
        buttons = self.driver.find_elements(*self._REMOVE_BTNS)
        buttons[index].click()
        return self

    def go_to_cart(self) -> None:
        """Click the cart icon and wait for cart page to load."""
        self.click(self._CART_ICON)
        self.wait_for_url_contains("cart.html")

    def logout(self) -> None:
        """Open burger menu and click logout."""
        self.click(self._BURGER_MENU)
        self.click(self._LOGOUT_LINK)

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_page_title(self) -> str:
        return self.get_text(self._PAGE_TITLE)

    def get_product_names(self) -> List[str]:
        elements = self.driver.find_elements(*self._PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self) -> List[float]:
        elements = self.driver.find_elements(*self._PRODUCT_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def get_cart_item_count(self) -> int:
        if not self.is_element_visible(self._CART_BADGE):
            return 0
        return int(self.get_text(self._CART_BADGE))

    def get_product_count(self) -> int:
        return len(self.driver.find_elements(*self._PRODUCT_ITEMS))

    def is_on_inventory_page(self) -> bool:
        return "inventory" in self.get_current_url()
