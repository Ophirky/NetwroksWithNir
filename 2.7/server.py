"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Server technician interaction app
"""
# Imports #
import socket as sock
import glob
import logging
import os
import protocol
from typing import Tuple, List


# Constants #
ERR_FOLDER_NOT_FOUND = "Folder not found"
ERR_FILE_NOT_FOUND = "File not found"

LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\server_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"


# Server class #
class Server:
    """
    Server class for handling client connections.
    """
    def __init__(self, host, port, queue_len) -> None:
        """
        Initialize the server object with host and port information.
        :param host: The hostname or IP address of the server.
        :param port: The port number of the server.
        :param queue_len: The queue length of the socket
        """
        self.host = host
        self.port = port
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)  # Create a socket object
        self.socket.bind((self.host, self.port))  # Bind the socket to the specified host and port
        self.socket.listen(queue_len)  # Listen for incoming connections

    def accept_connection(self) -> Tuple:
        """
        Accept a connection from a client.
        :return: tuple containing the client socket and the client ip
        """
        return self.socket.accept()

    def send_message(self, msg) -> None:
        self.socket.send(protocol.format_message(msg))

# Command Handler #
class Commands:
    """
    utility class that handles all the clients commands
    """
    # TODO: finish all of the commands
    @staticmethod
    def exit(client_socket: sock.socket, server: Server) -> None:
        """
        Closes the program
        :return: None
        """
        server.send_message("Disconnecting...")
        client_socket.close()

    @staticmethod
    def take_screenshot():
        pass

    @staticmethod
    def execute():
        pass

    @staticmethod
    def dir(path) -> List[str]:
        """
        Returns the contents of a folder
        :param path: the folder path
        :return:
        """
        if not os.path.isdir(path):
            logging.info(ERR_FOLDER_NOT_FOUND)
            return [ERR_FOLDER_NOT_FOUND]

        folder_content = glob.glob(path+"\\*.*")
        return path + ":" + "".join([f'\n\t{i}' for i in folder_content] if folder_content != [] else "Null")

    @staticmethod
    def copy():
        pass

    @staticmethod
    def delete(file_path) -> str:
        """
        deletes a file according to the given path
        :param file_path: the file path
        :return: success\fail message
        """
        try:
            os.remove(file_path)
        except FileNotFoundError:
            logging.error(ERR_FILE_NOT_FOUND)
            return ERR_FILE_NOT_FOUND
        except Exception as err:
            logging.exception(err)
            return str(err)

    # TODO: Add the command handling
    @staticmethod
    def handle_command(client, command, args) -> None:
        """
        Handles the commands given from the client
        :param client: The client socket and ip - tuple(socket.socket(), str)
        :param command: the given command from the client -> str
        :param args: The arguments given to the command by the client -> tuple
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
