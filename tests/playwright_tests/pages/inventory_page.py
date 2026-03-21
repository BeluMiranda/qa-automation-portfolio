"""
Page: InventoryPage (Playwright) — saucedemo.com/inventory.html
"""
from typing import List
from playwright.sync_api import Page

from tests.playwright_tests.pages.base_page import BasePage


class InventoryPage(BasePage):
    """Inventory page using Playwright."""

    _PAGE_TITLE = ".title"
    _SORT_DROPDOWN = ".product_sort_container"
    _PRODUCT_NAMES = ".inventory_item_name"
    _PRODUCT_PRICES = ".inventory_item_price"
    _CART_BADGE = ".shopping_cart_badge"
    _CART_ICON = ".shopping_cart_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_page_title(self) -> str:
        return self.get_text(self._PAGE_TITLE)

    def get_product_names(self) -> List[str]:
        return self.page.locator(self._PRODUCT_NAMES).all_inner_texts()

    def get_product_prices(self) -> List[float]:
        texts = self.page.locator(self._PRODUCT_PRICES).all_inner_texts()
        return [float(t.replace("$", "")) for t in texts]

    def add_to_cart(self, index: int = 0) -> None:
        self.page.locator("[data-test^='add-to-cart']").nth(index).click()

    def get_cart_count(self) -> int:
        if not self.is_visible(self._CART_BADGE):
            return 0
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self) -> None:
        self.click(self._CART_ICON)

    def sort_by(self, value: str) -> None:
        self.page.select_option(self._SORT_DROPDOWN, value)

    def is_on_page(self) -> bool:
        return "inventory" in self.get_current_url()
