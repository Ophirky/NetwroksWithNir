"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: File handling class
"""
import os.path
# Imports #
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

    def write_data(self) -> None:
        """
        Write data to the file
        :return: None
        """
        with open(self.name + self.__extension, 'wb') as f:
            pickle.dump(self.db, f)
            LOGGER.debug('Data written')
