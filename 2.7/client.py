"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Remote server interaction interface
"""
# Imports #
import socket as sock
import logging
import os
import protocol
import client_functions


# Constants #
LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\client_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

SUCC_SCREENSHOT = "screenshot taken"

IP = "127.0.0.1"
PORT = 5500

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

    def send_command(self, msg) -> None:
        """
        Sends a message to the server
        :param msg: the msg send to the server
        :return: None
        """
        self.sock.send(protocol.format_message(msg))

    def close(self) -> None:
        """
        Closes the connection
        :return: None
        """
        self.sock.close()

def main() -> None:
    """
    The main function for the server file
    :return: None
    """
    socket = Client(IP, PORT)
    try:

        socket.connect()

        while True:
            # Getting user input #
            user_in = input("Enter a command: ").upper()

            # Sending the user input to the server #
            if client_functions.validate_msg(user_in):
                socket.send_command(user_in)
            else:
                print("invalid command")
                continue

            # Receiving answer from server #
            if user_in.startswith("EXIT"):
                break

            server_ans = protocol.deformat_message(socket.sock)
            if user_in.startswith('TAKE_SCREENSHOT') and server_ans[0]:
                client_functions.save_image_to_file(server_ans[1])
                print(SUCC_SCREENSHOT)
            else:
                # Printing the server answer #
                print(server_ans[1].decode())

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
