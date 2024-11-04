"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This is the main file of the project
"""

# Imports #
import unittest
import os
from global_varaibles import LOGGER
from tests.test_database_sync_processes import DbSynchronizerTests


if __name__ == '__main__':
    # Running the tests #
    # start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    # unittest.main(module=None, argv=['first-arg-is-ignored', 'discover', start_dir], exit=False)
    tests = DbSynchronizerTests()
    tests.run_tests()

    # Delete test files #
    # os.remove('test_db.pkl')
    # os.remove('test_threads.pkl')
    #os.remove('test_processes.pkl')
    # os.remove('tmp_db_threads.pkl')
    os.remove('tmp_db_processes.pkl')

    LOGGER.debug("Tests complete")
