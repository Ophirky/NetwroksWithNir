"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This file will contain the main class for the sync of the threads / precesses
"""

# Imports #
from typing import Any

from operation_methods import OperationSettings
from global_varaibles import LOGGER
from thread_synchronizer import ThreadSync
from process_synchronizer import ProcessSync


class DbSynchronizer:
    """First layer of the syncer"""

    def __init__(self, operation_method: OperationSettings, name: str) -> None:
        """
        Constructor of the first layer handler.
        :param operation_method: the operation method to test.
        :param name: name for the db.
        :return: None
        """
        LOGGER.debug(f'method chosen: {operation_method}')
        match operation_method:
            case OperationSettings.THREADS:
                self.method = ThreadSync(name)

            case OperationSettings.PROCESSES:
                self.method = ProcessSync(name)

            case _:
                raise ValueError('Operation method not recognized')

    def read_from_db(self, key: Any) -> Any:
        """
        Get a certain value from the db
        :param key: the key to find.
        :return: the value from the given key
        """
        return self.method.read_from_db(key)

    def write_to_db(self, key: Any, value: Any) -> bool:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :param value: the value
        :return: successful or not
        """
        return self.method.write_to_db(key, value)
