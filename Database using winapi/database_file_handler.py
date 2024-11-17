"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: File handling class
"""
# Imports #
import os.path
import win32file
import pywintypes
import pickle

from database import Database
from global_varaibles import LOGGER


# File Handler #
class DbFileHandler(Database):
    """Handling file reading for the database"""

    def __init__(self, name: str) -> None:
        """
        Initializer of the FileHandler class
        :param name: The name for the database and the file.
        :return: None
        """
        super().__init__(name)
        self.__extension = '.pkl'

        if not self.__check_file_exists():
            self.write_data()

    def __check_file_exists(self) -> bool:
        """
        Check if file exists
        :return: Whether the file exists or not
        """
        # Try to open file #
        res = False
        try:
            file_handle = win32file.CreateFile(
                self.name + self.__extension,
                win32file.GENERIC_READ, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            win32file.CloseHandle(file_handle)
            res = True
        except pywintypes.error as e:
            if e.winerror != 2:
                LOGGER.error(e)
                raise

        return res

    def get_data(self) -> dict or None:
        """
        Will read the data from the file.
        :return: The database in dictionary form.
        """
        res = None

        file_handle = win32file.CreateFile(
            self.name + self.__extension,
            win32file.GENERIC_READ, 0, None,
            win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
        )

        # Reading the file #
        _, byte_data = win32file.ReadFile(file_handle, win32file.GetFileSize(file_handle))
        LOGGER.debug("Read from file complete")

        # Close Handle #
        win32file.CloseHandle(file_handle)
        LOGGER.debug("File Handle Closed")

        # Converting into data #
        try:
            res = pickle.loads(byte_data)
            LOGGER.debug('Converted data to dict')

        except EOFError as e:
            LOGGER.debug(e)

        return res

    def write_data(self) -> bool:
        """
        Write data to the file
        :return: successful or not
        """
        res = True
        try:
            file_handle = win32file.CreateFile(
                self.name + self.__extension,
                win32file.GENERIC_WRITE, 0, None,
                win32file.CREATE_ALWAYS, win32file.FILE_ATTRIBUTE_NORMAL, None
            )

            # Write to file #
            win32file.WriteFile(file_handle, pickle.dumps(self.db))
            LOGGER.debug('Written to file')

            # Close Handle #
            win32file.CloseHandle(file_handle)
            LOGGER.debug('File Handle Closed')

        except pywintypes.error as e:
            if e == 2:
                res = False
            else:
                LOGGER.error(e)
                raise

        return res
