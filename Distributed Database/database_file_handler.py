"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: File handling class
"""
# Imports #
import os.path
from database import Database
from global_varaibles import LOGGER
import pickle

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

        if not os.path.isfile(self.name + self.__extension):
            self.write_data()

    def get_data(self) -> dict or None:
        """
        Will read the data from the file.
        :return: The database in dictionary form.
        """
        res = None

        with open(self.name + self.__extension, 'rb') as f:
            try:
                res = pickle.load(f)
                LOGGER.debug('Got data')

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
            with open(self.name + self.__extension, 'wb') as f:
                pickle.dump(self.db, f)
                LOGGER.debug('Data written')
        except FileNotFoundError as e:
            res = False

        return res
