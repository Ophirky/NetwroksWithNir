"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Global project variables and constants
"""

# Imports #
import logging

# Constants #
GLOBAL_LOG_DIR = "Logs"
GLOBAL_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
GLOBAL_LOG_LEVEL = logging.DEBUG

LOGGER_NAME = 'main'
LOGGER = logging.getLogger(LOGGER_NAME)
LOG_FILE = GLOBAL_LOG_DIR + f"\\{LOGGER_NAME}.log"

# Setting up logger #
LOGGER.setLevel(GLOBAL_LOG_LEVEL)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter(GLOBAL_LOG_FORMAT))
LOGGER.addHandler(file_handler)
