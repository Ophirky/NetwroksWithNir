"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: This file will contain the main class for the sync of the threads / precesses
"""

# Imports #
import win32event
import win32con
from typing import Any

from global_varaibles import LOGGER
from database_file_handler import DbFileHandler

# Constants #
MAX_READERS = 10
INFINITE = -1


class DbSynchronizer(DbFileHandler):
    """First layer of the syncer"""

    def __init__(self, name: str) -> None:
        """
        Constructor of the first layer handler.
        :param name: name for the db.
        :return: None
        """
        super().__init__(name)
        self.write_lock = win32event.CreateMutex(None, False, None)
        self.reader_lock = win32event.CreateSemaphore(None, MAX_READERS, MAX_READERS, None)
        self.waiting_for_writer = win32event.CreateEvent(None, True, True, None)

    def read_from_db(self, key: Any) -> Any:
        """
        Get a certain value from the db
        :param key: the key to find.
        :return: the value from the given key
        """
        res = None
        # Waiting for there to be no writer #
        win32event.WaitForSingleObject(self.waiting_for_writer, INFINITE)

        # Start reading #
        LOGGER.debug('No writer')
        win32event.WaitForSingleObject(self.reader_lock, INFINITE)
        LOGGER.debug('Acquired reader lock')
        res = self.get_value(key)
        win32event.ReleaseSemaphore(self.reader_lock, 1)

        return res

    def write_to_db(self, key: Any, value: Any) -> bool:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :param value: the value
        :return: successful or not
        """
        res = True

        win32event.WaitForSingleObject(self.write_lock, INFINITE)
        try:
            # Owning all the read locks #
            win32event.ResetEvent(self.waiting_for_writer)
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

            win32event.SetEvent(self.waiting_for_writer)

        finally:
            # Releasing read locks #
            self.__release_all_readers()
            win32event.ReleaseMutex(self.write_lock)

        return res

    def delete_from_db(self, key: Any) -> Any:
        """
        Add to or change a value in db.
        :param key: the key to add / change
        :return: Value deleted
        """
        res = True
        win32event.WaitForSingleObject(self.write_lock, INFINITE)
        try:
            # Owning all the read locks #
            win32event.ResetEvent(self.waiting_for_writer)
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

                win32event.SetEvent(self.waiting_for_writer)

        finally:
            # Releasing read locks #
            self.__release_all_readers()
            win32event.ReleaseMutex(self.write_lock)

        return res

    # Private methods #
    def __lock_all_readers(self) -> None:
        """
        Locks al the reader slots
        :return: None
        """
        for i in range(MAX_READERS):
            win32event.WaitForSingleObject(self.reader_lock, INFINITE)
        LOGGER.debug("acquired all reader slots")

    def __release_all_readers(self) -> None:
        """
        Releases al the reader slots
        :return: None
        """
        for i in range(MAX_READERS):
            win32event.ReleaseSemaphore(self.reader_lock, 1)
        LOGGER.debug("released all reader slots")
