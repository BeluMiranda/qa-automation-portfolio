"""
Utility: Configuration Manager
Centralizes all environment variables and settings for the framework.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BrowserConfig:
    name: str = field(default_factory=lambda: os.getenv("BROWSER", "chrome"))
    headless: bool = field(default_factory=lambda: os.getenv("HEADLESS", "true").lower() == "true")
    implicit_wait: int = field(default_factory=lambda: int(os.getenv("IMPLICIT_WAIT", "10")))
    explicit_wait: int = field(default_factory=lambda: int(os.getenv("EXPLICIT_WAIT", "15")))
    page_load_timeout: int = field(default_factory=lambda: int(os.getenv("PAGE_LOAD_TIMEOUT", "30")))
    screenshot_on_failure: bool = field(
        default_factory=lambda: os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    )


@dataclass
class SauceDemoConfig:
    url: str = field(default_factory=lambda: os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com"))
    standard_user: str = field(default_factory=lambda: os.getenv("SAUCEDEMO_USER", "standard_user"))
    password: str = field(default_factory=lambda: os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce"))
    locked_user: str = field(default_factory=lambda: os.getenv("SAUCEDEMO_LOCKED_USER", "locked_out_user"))
    problem_user: str = field(default_factory=lambda: os.getenv("SAUCEDEMO_PROBLEM_USER", "problem_user"))
    perf_user: str = field(
        default_factory=lambda: os.getenv("SAUCEDEMO_PERF_USER", "performance_glitch_user")
    )


@dataclass
class APIConfig:
    jsonplaceholder_url: str = field(
        default_factory=lambda: os.getenv("JSONPLACEHOLDER_URL", "https://jsonplaceholder.typicode.com")
    )
    dummyjson_url: str = field(default_factory=lambda: os.getenv("DUMMYJSON_URL", "https://dummyjson.com"))
    timeout: int = 10
    retry_count: int = field(default_factory=lambda: int(os.getenv("RETRY_COUNT", "2")))


@dataclass
class Settings:
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    saucedemo: SauceDemoConfig = field(default_factory=SauceDemoConfig)
    api: APIConfig = field(default_factory=APIConfig)
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    reports_dir: str = "reports"
    screenshots_dir: str = "reports/screenshots"
    allure_results_dir: str = "allure-results"


# Singleton instance — import this across the codebase
settings = Settings()
