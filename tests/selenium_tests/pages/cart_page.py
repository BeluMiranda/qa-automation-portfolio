"""
Page: CartPage — saucedemo.com/cart.html
Page: CheckoutStepOnePage — saucedemo.com/checkout-step-one.html
Page: CheckoutStepTwoPage — saucedemo.com/checkout-step-two.html
Page: CheckoutCompletePage — saucedemo.com/checkout-complete.html
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tests.selenium_tests.pages.base_page import BasePage


class CartPage(BasePage):
    """Represents the Cart page."""

    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _REMOVE_BTNS = (By.CSS_SELECTOR, "[data-test^='remove']")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_item_names(self) -> List[str]:
        elements = self.driver.find_elements(*self._ITEM_NAMES)
        return [el.text for el in elements]

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def remove_item(self, index: int = 0) -> "CartPage":
        initial = self.get_item_count()
        buttons = self.driver.find_elements(*self._REMOVE_BTNS)
        self.driver.execute_script("arguments[0].click();", buttons[index])
        if initial > 0:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_elements(*self._CART_ITEMS)) < initial
            )
        return self

    def proceed_to_checkout(self) -> None:
        btn = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self._CHECKOUT_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 30).until(EC.url_contains("checkout-step-one"))

    def continue_shopping(self) -> None:
        self.click(self._CONTINUE_SHOPPING)

    def is_cart_empty(self) -> bool:
        return self.get_item_count() == 0

    def is_cart_page(self) -> bool:
        return "cart" in self.get_current_url()


class CheckoutStepOnePage(BasePage):
    """Represents the Checkout Step 1 page (customer info)."""

    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _CANCEL_BTN = (By.ID, "cancel")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def fill_customer_info(self, first: str, last: str, postal: str) -> "CheckoutStepOnePage":
        # SauceDemo uses React controlled inputs. Standard send_keys does not update React state.
        # We directly dispatch values to the React fiber useState hooks and then call the form's
        # onSubmit handler (which is what the Continue button ultimately triggers).
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located(self._FIRST_NAME))
        self.driver.execute_script(
            """
            var first = arguments[0], last = arguments[1], postal = arguments[2];
            var form = document.querySelector('form');
            var fiberKey = Object.keys(form).find(k => k.startsWith('__reactFiber'));
            var fiber = form[fiberKey].return;
            while (fiber) {
                if (fiber.memoizedState) {
                    var hooks = [];
                    var h = fiber.memoizedState;
                    while (h) { hooks.push(h); h = h.next; }
                    var sh = hooks.filter(function(h) {
                        return typeof h.memoizedState === 'string' && h.queue && h.queue.dispatch;
                    });
                    if (sh.length >= 3) {
                        sh[0].queue.dispatch(first);
                        sh[1].queue.dispatch(last);
                        sh[2].queue.dispatch(postal);
                        break;
                    }
                }
                fiber = fiber.return;
            }
            """,
            first, last, postal
        )
        return self

    def click_continue(self) -> None:
        import time
        time.sleep(0.5)  # allow React to process dispatched state updates
        self.driver.execute_script(
            """
            var form = document.querySelector('form');
            var propsKey = Object.keys(form).find(k => k.startsWith('__reactProps'));
            if (form[propsKey] && form[propsKey].onSubmit) {
                form[propsKey].onSubmit({
                    preventDefault: function(){},
                    stopPropagation: function(){},
                    target: form
                });
            }
            """
        )
        self.wait_for_url_contains("checkout-step-two")

    def click_cancel(self) -> None:
        self.driver.execute_script(
            """
            var btn = document.getElementById('cancel');
            var pk = Object.keys(btn).find(k => k.startsWith('__reactProps'));
            btn[pk].onClick({
                preventDefault: function(){},
                stopPropagation: function(){},
                target: btn
            });
            """
        )
        self.wait_for_url_contains("cart")

    def get_error(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def has_error(self) -> bool:
        return self.is_element_visible(self._ERROR_MSG)


class CheckoutStepTwoPage(BasePage):
    """Represents the Order Summary page (step 2)."""

    _ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    _TAX = (By.CLASS_NAME, "summary_tax_label")
    _TOTAL = (By.CLASS_NAME, "summary_total_label")
    _FINISH_BTN = (By.ID, "finish")
    _CANCEL_BTN = (By.ID, "cancel")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_item_total(self) -> str:
        return self.get_text(self._ITEM_TOTAL)

    def get_tax(self) -> str:
        return self.get_text(self._TAX)

    def get_total(self) -> str:
        return self.get_text(self._TOTAL)

    def get_item_count(self) -> int:
        try:
            self.find_element(self._CART_ITEMS)  # wait for first item to appear
        except TimeoutException:
            return 0
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def click_finish(self) -> None:
        self.driver.execute_script(
            """
            var btn = document.getElementById('finish');
            var propsKey = Object.keys(btn).find(k => k.startsWith('__reactProps'));
            btn[propsKey].onClick({
                preventDefault: function(){},
                stopPropagation: function(){},
                target: btn
            });
            """
        )
        self.wait_for_url_contains("checkout-complete")

    def click_cancel(self) -> None:
        self.click(self._CANCEL_BTN)


class CheckoutCompletePage(BasePage):
    """Represents the Order Complete confirmation page."""

    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    _BACK_HOME_BTN = (By.ID, "back-to-products")
    _PONY_IMG = (By.CLASS_NAME, "pony_express")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_complete_header(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        return self.get_text(self._COMPLETE_TEXT)

    def back_to_home(self) -> None:
        self.driver.execute_script(
            """
            var btn = document.getElementById('back-to-products');
            var pk = Object.keys(btn).find(k => k.startsWith('__reactProps'));
            btn[pk].onClick({
                preventDefault: function(){},
                stopPropagation: function(){},
                target: btn
            });
            """
        )
        self.wait_for_url_contains("inventory")

    def is_order_complete(self) -> bool:
        return "Thank you" in self.get_complete_header()
