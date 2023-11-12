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


def protocol_format(msg: str) -> str:
    """
    Formats the msg to fit the protocol
    :param msg: the msg to send
    :return: None
    """
    return PROTOCOL_FORMAT.format(msg_len=len(msg), msg=msg)


def protocol_deformat(formatted_msg: str) -> List:
    """
    returns the separated msg in a list
    :param formatted_msg: the protocol formatted msg
    :return List[int, string]: {len, msg}
    """
    return formatted_msg.split("|")


# Client code #
def main() -> None:
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    try:
        socket.connect((IP, PORT))
        print(socket.recv(MAX_PACKET).decode())

        while True:
            # Getting user input #
            user_in = protocol_format(input("Enter a command: "))

            # Validating #
            if len(user_in) > 6:
                print("Invalid input")
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
    assert protocol_format("msg") == PROTOCOL_FORMAT.format(msg_len=len("msg"), msg="msg")
    assert protocol_deformat(f"{len('msg')}|msg") == f"{len('msg')}|msg".split("|")

    # Running main code #
    main()
