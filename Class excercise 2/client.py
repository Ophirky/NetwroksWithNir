"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/4/2023
    DESCRIPTION: simple remote command line client.
"""

# Imports #
import socket as sock
import logging
import os

# Constants #
IP = "127.0.0.1"
PORT = 5500
MAX_PACKET = 1024

LOG_FORMAT = "%(levelname)s | %(asctime)s | %(processName)s | %(msg)s"
LOG_LEVEL = logging.DEBUG
LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/log.log"

# Client code #
def main() -> None:
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    try:
        socket.connect((IP, PORT))
        print(socket.recv(MAX_PACKET).decode())

        while True:
            # Getting user input #
            user_in = input("Enter a command: ")

            # Validating input #
            if len(user_in) > 4 or len(user_in) < 4:
                print("Invalid input")
                continue

            socket.send(user_in.encode())

            server_ans = socket.recv(MAX_PACKET).decode()

            print(server_ans)
            if server_ans == 'Disconnecting...':
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

    # Running main code #
    main()
