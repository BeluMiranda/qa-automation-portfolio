"""
conftest.py - Selenium Tests
Fixtures centralizados para el suite de Selenium.
El driver es creado una vez por sesión de test y destruido al finalizar.
"""
import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def _chrome_driver() -> webdriver.Chrome:
    options = ChromeOptions()
    if settings.browser.headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Fix: webdriver-manager a veces apunta al archivo incorrecto
    driver_path = ChromeDriverManager().install()
    if not driver_path.endswith("chromedriver.exe"):
        import os
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

    service = ChromeService(driver_path)
    return webdriver.Chrome(service=service, options=options)


def _firefox_driver() -> webdriver.Firefox:
    options = FirefoxOptions()
    if settings.browser.headless:
        options.add_argument("--headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture: WebDriver per test function.
    Scope=function guarantees test isolation.
    Attaches screenshot to Allure on failure.
    """
    browser = settings.browser.name.lower()
    logger.info("Initializing browser", extra={"browser": browser})

    if browser == "firefox":
        _driver = _firefox_driver()
    else:
        _driver = _chrome_driver()

    _driver.implicitly_wait(settings.browser.implicit_wait)
    _driver.set_page_load_timeout(settings.browser.page_load_timeout)

    yield _driver

    # ---- Teardown ----
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        if settings.browser.screenshot_on_failure:
            _take_screenshot(_driver, request.node.name)

    logger.info("Closing browser", extra={"browser": browser})
    _driver.quit()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Returns the base URL for Sauce Demo."""
    return settings.saucedemo.url


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to track test result for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _take_screenshot(driver: webdriver.Chrome, test_name: str) -> None:
    """Saves a screenshot and attaches it to the Allure report."""
    os.makedirs(settings.screenshots_dir, exist_ok=True)
    path = os.path.join(settings.screenshots_dir, f"{test_name}.png")
    driver.save_screenshot(path)
    allure.attach.file(
        path,
        name=f"Failure: {test_name}",
        attachment_type=allure.attachment_type.PNG,
    )
    logger.info("Screenshot saved", extra={"path": path})
