"""
Page: BasePage
Clase base con métodos comunes (wait, click, send_keys, etc.)
Toda page object hereda de esta clase — nunca interactúa con el driver directamente.
"""
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Base Page Object.
    All page classes inherit from here to reuse driver interactions.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.browser.explicit_wait)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open(self, url: str) -> None:
        """Navigate to a URL."""
        logger.info("Navigating", extra={"url": url})
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ------------------------------------------------------------------
    # Element interactions
    # ------------------------------------------------------------------

    def find_element(self, locator: tuple) -> WebElement:
        """Wait for element to be present and return it."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error("Element not found", extra={"locator": str(locator)})
            raise

    def find_visible_element(self, locator: tuple) -> WebElement:
        """Wait for element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable_element(self, locator: tuple) -> WebElement:
        """Wait for element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple) -> None:
        """Click an element once it is clickable."""
        element = self.find_clickable_element(locator)
        logger.debug("Clicking element", extra={"locator": str(locator)})
        element.click()

    def type_text(self, locator: tuple, text: str) -> None:
        """Type into a field. W3C send_keys focuses the element automatically."""
        element = self.find_visible_element(locator)
        element.send_keys(text)
        logger.debug("Typed text", extra={"locator": str(locator), "text": text})

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        return self.find_visible_element(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Return an element attribute value."""
        return self.find_element(locator).get_attribute(attribute)

    def is_element_visible(self, locator: tuple) -> bool:
        """Return True if element is visible, False otherwise (no exception)."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Return True if element is present in DOM (may be hidden)."""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, url_fragment: str) -> bool:
        """Wait until current URL contains a fragment."""
        try:
            return self.wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            return False

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Take a screenshot and attach it to Allure."""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        return screenshot
