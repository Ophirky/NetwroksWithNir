"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/2/2023
    DESCRIPTION: simple remote command line server.
"""
# Imports #
import datetime as dt
import logging
import os
import random as ran
import socket as sock

# Constants #
IP = "0.0.0.0"
PORT = 5500
MAX_PACKET = 4
QUEUE_LEN = 1

LOG_FORMAT = "%(levelname)s | %(asctime)s | %(processName)s | %(msg)s"
LOG_LEVEL = logging.DEBUG
LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/log.log"

ERR_UNKNOWN_COMMAND = "Unknown Command"


# Commands Class #
class Commands:
    commands = {
        "TIME": "Sends the time",
        "NAME": "Sends the command lines name",
        "RAND": "returns a random number between 1-10",
        "EXIT": "disconnects the client"
    }

    @staticmethod
    def comm_time() -> str:
        """
        :return str: returns the current time
        """
        return dt.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def comm_name() -> str:
        """
        :return str: returns command lines' name
        """
        return "Johnny"

    @staticmethod
    def comm_rand() -> int:
        """
        rolls a d6 dice
        :return int: number between 1 & 6
        """
        return ran.randint(1, 6)

    @staticmethod
    def comm_exit(client_socket: sock.socket) -> None:
        """
        Closes the program
        :return: None
        """
        client_socket.send("Disconnecting...".encode())
        client_socket.close()


def client_handle(socket: sock.socket):
    try:
        # Connecting to the socket #
        socket.bind((IP, PORT))

        # waiting for client connection & getting client info #
        socket.listen(QUEUE_LEN)
        client_socket, client_ip = socket.accept()

        # Sending the command list #
        client_socket.send(f"{Commands.commands=}".encode())

        try:
            while True:
                # Command handling #
                match client_socket.recv(MAX_PACKET).decode().upper():
                    # TIME - sends back the current time #
                    case 'TIME':
                        client_socket.send(Commands.comm_time().encode())

                    # NAME - sends back the name of the command prompt #
                    case 'NAME':
                        client_socket.send(Commands.comm_name().encode())

                    # RAND - sends back a random number between 1 & 10 #
                    case 'RAND':
                        client_socket.send(str(Commands.comm_rand()).encode())

                    # EXIT - disconnects the client from the server #
                    case 'EXIT':
                        Commands.comm_exit(client_socket)
                        client_handle(socket)

                    # Default - unknown command #
                    case _:
                        client_socket.send(ERR_UNKNOWN_COMMAND)

        except Exception as err:
            logging.exception(err)

        finally:
            client_socket.close()

    except sock.error as err:
        logging.exception(err)

    finally:
        socket.close()


# Main Server Code #
def main() -> None:
    # socket creation #
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    # handling client #
    client_handle(socket)


if __name__ == '__main__':
    # Logging handling #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # Running main code #
    main()
