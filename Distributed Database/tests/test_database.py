"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Unit test for the Database class
"""

# Imports #
import unittest
import database
from log_manager import LOGGER


class TestDatabase(unittest.TestCase):
    """Testing the Database class"""

    def test_set_value(self) -> None:
        """
        Testing the set_value function.
        :return: None
        """
        db = database.Database('test')

        # Adding a value #
        key, value = 'name', 'Ophir'
        res = db.set_value(key, value)
        self.assertTrue(res)
        self.assertEqual(value, db.get_value(key))

        # Adding another value #
        key, value = 'age', 17
        res = db.set_value(key, value)
        self.assertTrue(res)

        LOGGER.debug("Adding value test complete")

        # Testing dictionary #
        self.assertEqual(db.db, {'name': 'Ophir', 'age': 17})

        # Changing a value #
        value = 19
        res = db.set_value(key, value)
        self.assertTrue(res)

        LOGGER.debug("Changing value test complete")

        # Testing dictionary #
        self.assertEqual(db.db, {'name': 'Ophir', 'age': 19})

    def test_get_value(self) -> None:
        """
        Testing the get_value function.
        :return: None
        """
        key, value = 'name', 'Ophir'
        db = database.Database('test')
        db.set_value(key, value)

        # Getting a value #
        res = db.get_value(key)
        self.assertEqual(res, value)
        LOGGER.debug("Get value test complete")

    def test_delete_value(self) -> None:
        """
        Testing the delete_value function.
        :return: None
        """
        key, value = 'name', 'Ophir'
        db = database.Database('test')
        db.set_value(key, value)

        # Removing the value #
        res = db.delete_value(key)
        self.assertEqual(res, value)

        # Checking if the value is deleted #
        self.assertEqual(db.db, {})

        LOGGER.debug("Delete value test complete")

