"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This file contains the database class that is responsible for interacting with the database
                 in dictionary form.
"""

# Imports #
from typing import Any
from global_varaibles import LOGGER

# Database Class #
class Database:
    """responsible for interacting with the database in dictionary form"""

    def __init__(self, name: str) -> None:
        """
        Constructor of the Database class
        :param name: the name of the db
        :return: None
        """
        self.name = name
        self.db: dict = {}

    def set_value(self, key: Any, value: Any) -> bool:
        """
        This will handle adding and changing values in the database.
        :param key: The key to change.
        :param value: the value to set.
        :return bool: whether the operation was successful
        """
        res = True
        try:
            self.db[key] = value
            LOGGER.debug('Value added to dictionary')
        except KeyError:
            res = False
            LOGGER.debug('Value adding failed')

        return res

    def get_value(self, key: Any) -> Any:
        """
        Get a value from the db.
        :param key: The key that stores the wanted value.
        :return: The value in the given key or None if nonexistent.
        """
        res = self.db.get(key, None)
        LOGGER.debug(f'Got value from dict - {res}')
        return res

    def delete_value(self, key: Any) -> Any:
        """
        delete a key and value from the db.
        :param key: The key that stores the wanted value.
        :return: The value in the given key or None if nonexistent.
        """
        res = None
        try:
            res = self.db[key]
            del self.db[key]
            LOGGER.debug('Deleted value from dict')
        except KeyError:
            res = None
            LOGGER.debug('Deletion failed')

        return res
