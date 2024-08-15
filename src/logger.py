import logging
import logging.handlers
import os

from src.config import LOGS_DIRECTORY


def setup_logger(name, level=logging.INFO):
    """To setup loggers with logs organized by date, it will auto rotate at midnight"""
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    log_file = os.path.join(f"{LOGS_DIRECTORY}/{name}.log")

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


LOGGER = setup_logger("log")
