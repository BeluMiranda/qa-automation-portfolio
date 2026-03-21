"""
Utility: Logger
Structured JSON logging for the automation framework.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from utils.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with JSON formatting for CI/CD compatibility.

    Usage:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Test started", extra={"test": "test_login"})
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
