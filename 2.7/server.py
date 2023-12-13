"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Server technician interaction app
"""
# Imports #
import socket as sock
import server_functions
import logging
import os
import protocol
from typing import Tuple

# Constants #
ERR_FOLDER_NOT_FOUND = "Folder not found"
ERR_FILE_NOT_FOUND = "File not found"

IP = "0.0.0.0"
PORT = 5500
QUEUE_LEN = 1

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

    def send_message(self, client_socket: sock.socket, msg) -> None:
        """
        sends a message to The client.
        :param client_socket: The socket that the msg is for.
        :param msg: the msg that is meant to be sent.
        :return: None
        """
        client_socket.send(protocol.format_message(msg))

# Main Server Code #
def main() -> None:
    # socket creation #
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    # handling client #
    try:
        # Starting the server #
        server = Server(IP, PORT, QUEUE_LEN)

        # Client Handle #
        while True:
            # Getting the client information and connection #
            client_socket, client_ip = server.accept_connection()
            print(f"client connected: {client_ip}")

            try:
                # Getting and handling the user input #
                while True:
                    # Getting the message from the client #
                    user_input = protocol.deformat_message(client_socket)

                    try:
                        # Handling the commands from the client #
                        match user_input[0].decode().upper():
                            case 'DELETE':
                                server.send_message(client_socket, server_functions.delete(user_input[1].decode()))
                            case 'EXECUTE':
                                server.send_message(client_socket, server_functions.execute(user_input[1].decode()))
                            case 'DIR':
                                server.send_message(client_socket, server_functions.delete(user_input[1].decode()))
                            case 'TAKE_SCREENSHOT':
                                server.send_message(client_socket, server_functions.take_screenshot())
                            case 'EXIT':
                                server_functions.exit_client(client_socket)
                                break

                    except sock.error as err:
                        logging.error(err)

                    except Exception as err:
                        server.send_message(client_socket, "False " + str(err))
                        logging.exception(err)

            except Exception as err:
                logging.exception(err)

            finally:
                client_socket.close()

    except sock.error as err:
        logging.exception(err)

    finally:
        socket.close()


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
