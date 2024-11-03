"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Handles thread synchronizing
"""

# Imports #
from typing import Any

from database_file_handler import DbFileHandler


class ThreadSync(DbFileHandler):
    """Thread Sync Handler"""

    def __init__(self, name: str) -> None:
        """
        Constructor of the Thread handler.
        :param name: name for the db.
        :return: None
        """
        super().__init__(name)

    def read_from_db(self, key: Any) -> Any:
        """
        Get a certain value from the db
        :param key: the key to find.
        :return: the value from the given key
        """
        ...

    def write_to_db(self, key: Any, value: Any) -> bool:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :param value: the value
        :return: successful or not
        """
        ...
