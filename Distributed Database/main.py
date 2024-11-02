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
    LOGGER.debug("Tests complete")

    db = DbFileHandler('Human')

    db.set_value('name', 'Ophir')
    db.set_value('age', 17)
    db.write_data()

    print(db.get_data())
