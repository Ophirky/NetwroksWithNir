"""
    AUTHOR: Ophir Nevo Michrowski.
    DESCRIPTION: Testing the file handler class.
"""
# Imports #
import os.path
import unittest
from database_file_handler import DbFileHandler
from log_manager import LOGGER


# Testcase #
class TestFileHandler(unittest.TestCase):
    """Testing the file handler"""

    DB_NAME: str = "test_db"
    EXTENSION: str = ".pkl"
    db = DbFileHandler(DB_NAME)

    def __get_file_content(self, filepath: str) -> bytes:
        """
        Get the contents of a file if any.
        :param filepath: the file path
        :return: the contents of the file
        """
        res: bytes

        if not os.path.isfile(filepath):
            res = b''
        else:
            with open(self.DB_NAME + self.EXTENSION, 'rb') as f:
                res = f.read()
            LOGGER.debug('File read was successful')

        return res

    def test_write(self) -> None:
        """
        Testing writing to the file
        :return: None
        """
        self.db.set_value("name", "Ophir")

        self.assertTrue(self.db.write_data())
        LOGGER.debug('Writing to file test finished')

        self.assertTrue(os.path.isfile(self.DB_NAME + self.EXTENSION))

        res: bytes = b''

        with open(self.DB_NAME + self.EXTENSION, 'rb') as f:
            res = f.read()
        LOGGER.debug('File read was successful')

        self.assertNotEqual(self.__get_file_content(self.DB_NAME + self.EXTENSION), b'')
        LOGGER.debug('Testing file contents after writing to file test finished')

    def test_read(self) -> None:
        """
        Testing the get_data function from the file.
        :return: None
        """
        self.db.set_value("name", "Ophir")
        self.db.write_data()

        self.assertEqual(self.db.get_data(), self.db.db)
        LOGGER.debug("Reading from file test complete")
