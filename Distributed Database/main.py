"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This is the main file of the project
"""

# Imports #
import unittest
import os
from global_varaibles import LOGGER
from database_file_handler import DbFileHandler


if __name__ == '__main__':
    # Running the tests #
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    unittest.main(module=None, argv=['first-arg-is-ignored', 'discover', start_dir], exit=False)

    # Delete test file #
    os.remove('test_db.pkl')

    LOGGER.debug("Tests complete")

