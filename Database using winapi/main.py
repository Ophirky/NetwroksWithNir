"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This is the main file of the project
"""

# Imports #
import unittest
import os
from global_varaibles import LOGGER
from tests.test_threads import DbSynchronizerTests

import win32file
import pywintypes

def delete_file(path: str) -> bool:
    """
    Deleting a file.
    :param path: The file path
    :return: successful or not
    """
    res = True
    try:
        win32file.DeleteFile(path)
    except pywintypes.error as e:
        res = False

    return res


if __name__ == '__main__':
    # Running the tests #
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    unittest.main(module=None, argv=['first-arg-is-ignored', 'discover', start_dir], exit=False)

    # Delete test files #
    delete_file('test_db.pkl')
    delete_file('test_tmp_processes.pkl')
    delete_file('test_processes.pkl')

    LOGGER.debug("Tests complete")
