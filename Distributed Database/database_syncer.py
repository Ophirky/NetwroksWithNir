"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This file will contain the main class for the sync of the threads / precesses
"""

# Imports #
import threading
import multiprocessing
from typing import Any

import operation_methods
from operation_methods import OperationSettings
from global_varaibles import LOGGER
from database_file_handler import DbFileHandler

# Constants #
MAX_READERS = 10


class DbSynchronizer(DbFileHandler):
    """First layer of the syncer"""

    def __init__(self, operation_method: OperationSettings, name: str) -> None:
        """
        Constructor of the first layer handler.
        :param operation_method: the operation method to test.
        :param name: name for the db.
        :return: None
        """
        super().__init__(name)
        LOGGER.debug(f'method chosen: {operation_method}')
        self.operation_method = operation_method

        match operation_method:
            case OperationSettings.THREADS:
                self.write_lock = threading.Lock()
                self.reader_lock = threading.Semaphore(MAX_READERS)
                self.waiting_for_writer = threading.Event()

                # Initial read of the file #
                self.db = self.get_data()

            case OperationSettings.PROCESSES:
                self.write_lock = multiprocessing.Lock()
                self.reader_lock = multiprocessing.Semaphore(MAX_READERS)
                self.waiting_for_writer = multiprocessing.Event()
                self.db = multiprocessing.Manager().dict(self.get_data())

            case _:
                raise ValueError('Operation method not recognized')

        # When event is set there is no writer and when event is clear there is a writer #
        self.waiting_for_writer.set()

    def read_from_db(self, key: Any) -> Any:
        """
        Get a certain value from the db
        :param key: the key to find.
        :return: the value from the given key
        """
        res = None
        # Waiting for there to be no writer #
        self.waiting_for_writer.wait(timeout=None)

        # Start reading #
        LOGGER.debug('No writer')
        with self.reader_lock:
            LOGGER.debug('Acquired reader lock')
            res = self.get_value(key)

        return res

    def write_to_db(self, key: Any, value: Any) -> bool:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :param value: the value
        :return: successful or not
        """
        res = True

        with self.write_lock:
            # Owning all the read locks #
            self.waiting_for_writer.clear()
            self.__lock_all_readers()

            # Setting the value #
            res = self.set_value(key, value)
            LOGGER.debug(f'adding {key}: {value} to db was {res}')

            # Writing to file #
            if res:
                res = self.write_data()
                LOGGER.debug('writing was ' + str(res))

                # If writing did not succeed - not keeping what file did not save #
                if not res:
                    self.delete_value(key)

            # Releasing read locks #
            self.waiting_for_writer.set()
            self.__release_all_readers()

        return res

    def delete_from_db(self, key: Any) -> Any:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :return: Value deleted
        """
        res = True

        with self.write_lock:
            # Owning all the read locks #
            self.waiting_for_writer.clear()
            self.__lock_all_readers()

            # Setting the value #
            res = self.delete_value(key)
            LOGGER.debug(f'deleted {key}')

            # Writing to file #
            success_writing = self.write_data()
            LOGGER.debug('writing was ' + str(res))

            # If writing did not succeed - keeping what wasn't deleted from file #
            if not success_writing:
                self.set_value(key, res)

            # Releasing read locks #
            self.waiting_for_writer.set()
            self.__release_all_readers()

        return res

    # Private methods #
    def __lock_all_readers(self) -> None:
        """
        Locks al the reader slots
        :return: None
        """
        for i in range(MAX_READERS):
            self.reader_lock.acquire()

    def __release_all_readers(self) -> None:
        """
        Releases al the reader slots
        :return: None
        """
        for i in range(MAX_READERS):
            self.reader_lock.release()
        LOGGER.debug("released all reader slots")
