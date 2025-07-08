import pytest
import logging

@pytest.fixture(autouse=True)
def silence_logger():
    logger = logging.getLogger("pipeline")
    previous_level = logger.level
    logger.setLevel(logging.CRITICAL + 1)  # Silencia todo
    yield
    logger.setLevel(previous_level)