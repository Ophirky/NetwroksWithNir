"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This is the main file of the project
"""

# Imports #
import unittest
import threading
import os
import time

import database_syncer
import operation_methods
from global_varaibles import LOGGER
from database_file_handler import DbFileHandler


def write(key, value, db):
    db.write_to_db(key, value)

def delete(key, db):
    db.delete_from_db(key)


def read(count, key, db):
    print(f"{count}, {db.read_from_db(key)}")


if __name__ == '__main__':
    # Running the tests #
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    unittest.main(module=None, argv=['first-arg-is-ignored', 'discover', start_dir], exit=False)

    # Delete test file #
    os.remove('test_db.pkl')

    LOGGER.debug("Tests complete")

    db = database_syncer.DbSynchronizer(operation_methods.OperationSettings.THREADS, 'testing')

    # threading.Thread(target=write, args=['name', 'ophir', db]).start()
    # threading.Thread(target=read, args=[0, "name", db]).start()
    # time.sleep(10)
    # threading.Thread(target=delete, args=['name', db]).start()
    # threading.Thread(target=read, args=[1, "name", db]).start()


