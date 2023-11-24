"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Remote server interaction interface
"""
# Imports #
import socket as sock
import logging
import os


# Constants #
LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\client_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"


# Client class #
class Client:
    """
    Client class for interacting with the server.
    """

    def __init__(self, host, port) -> None:
        """
        Initialize the client object with host and port information.
        :param host: The hostname or IP address of the server.
        :param port: The port number of the server.
        """
        self.host = host
        self.port = port
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)  # Create a socket object

    def connect(self) -> None:
        """
        Connect to the server.
        """
        try:
            self.sock.connect((self.host, self.port))  # Establish a connection to the server
        except sock.error as err:
            logging.error(err)
            print(err)
        except Exception as err:
            logging.exception(err)
            print(err)

    # TODO: add protocol format
    def send_command(self, command, args="") -> None:
        """
        Sends a message to the server
        :param command: the command given by the user
        :param args: the parameters of the func
        :return: None
        """

# TODO: Create the main function
def main() -> None:
    """
    The main function for the server file
    :return: None
    """
    pass


if __name__ == '__main__':
    # Testing if the logging folder exists #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Log setup #
    logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format=LOG_FORMAT)

    # Asserts #
    # TODO: Add asserts

    # Main function call #
    main()
