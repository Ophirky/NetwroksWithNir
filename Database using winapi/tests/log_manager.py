"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Creating the logger
"""

# Imports #
import logging
from global_varaibles import GLOBAL_LOG_LEVEL, GLOBAL_LOG_DIR, GLOBAL_LOG_FORMAT

# Constants #
LOGGER_NAME = 'tests'
LOGGER = logging.getLogger(LOGGER_NAME)
LOG_FILE = GLOBAL_LOG_DIR + f"\\{LOGGER_NAME}.log"

# Setting up logger #
LOGGER.setLevel(GLOBAL_LOG_LEVEL)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter(GLOBAL_LOG_FORMAT))
LOGGER.addHandler(file_handler)
