"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/4/2023
    DESCRIPTION: simple remote command line client.
"""

# Imports #
import socket as sock
import logging
import os
from typing import List

# Constants #
IP = "127.0.0.1"
PORT = 5500
MAX_PACKET = 1024

LOG_FORMAT = "%(levelname)s | %(asctime)s | %(processName)s | %(msg)s"
LOG_LEVEL = logging.DEBUG
LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/client_log.log"

PROTOCOL_FORMAT = "{msg_len}|{msg}"

ERR_INVALID_INPUT = "Invalid Input"


def protocol_deformat(formatted_msg: str) -> List:
    """
    returns the separated msg in a list
    :param formatted_msg: the protocol formatted msg
    :return List[int, string]: {len, msg}
    """
    return formatted_msg.split("|")


def validate_msg(msg: str) -> bool:
    """
    Checks if the message is a command
    :param msg: the user input
    :return: boolean if the message is valid
    """
    return True if msg.upper() == 'TIME' or msg.upper() == 'NAME' or msg.upper() == "RAND" or msg.upper() == "EXIT" \
        else False


# Client code #
def main() -> None:
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    try:
        socket.connect((IP, PORT))
        print(socket.recv(MAX_PACKET).decode())

        while True:
            # Getting user input #
            user_in = input("Enter a command: ")

            # Validating #
            if not validate_msg(user_in):
                print(ERR_INVALID_INPUT)
                continue

            # Sending the user input to the server #
            socket.send(user_in.encode())

            # Receiving answer from server #
            server_ans = protocol_deformat(socket.recv(MAX_PACKET).decode())

            # Printing the server answer #
            print(server_ans[1])

            # Checking exit protocol #
            if server_ans[1] == 'Disconnecting...':
                break

    except sock.error as err:
        logging.exception(err)

    finally:
        socket.close()


if __name__ == '__main__':
    # Logging handling #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # Automatic checks #
    assert protocol_deformat(f"{len('msg')}|msg") == f"{len('msg')}|msg".split("|")

    assert validate_msg("TIME")
    assert validate_msg("NAME")
    assert validate_msg("RAND")
    assert validate_msg("EXIT")

    # Running main code #
    main()
