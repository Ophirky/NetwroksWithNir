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
LOG_FILE = f"{LOG_DIR}/server_log.log"

ERR_RAND_ASSERTION = "Rand command not failed"
ERR_SERVER_NAME_ASSERTION = "Name command not working"
ERR_PROTOCOL_ASSERTION = "Protocol Formatting not working"

PROTOCOL_FORMAT = "{msg_len}|{msg}"
SERVER_NAME = "Parabot"


# Protocol functions #
def protocol_format(msg: str) -> str:
    """
    Formats the msg to fit the protocol
    :param msg: the msg to send
    :return: None
    """
    return PROTOCOL_FORMAT.format(msg_len=len(msg), msg=msg)


# Commands Class #
class Commands:
    global SERVER_NAME
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
        :return str: returns command lines name
        """
        return SERVER_NAME

    @staticmethod
    def comm_rand() -> int:
        """
        returns a number between 1 - 10
        :return int: number between 1 - 10
        """
        return ran.randint(1, 10)

    @staticmethod
    def comm_exit(client_socket: sock.socket) -> None:
        """
        Closes the program
        :return: None
        """
        client_socket.send(protocol_format("Disconnecting...").encode())
        client_socket.close()

    @staticmethod
    def command_validate_and_run(client_socket: tuple) -> None:
        """
        Handles the client input
        :param client_socket: tuple containing (client_ip: str, client_socket: sock.socket)
        :return:
        """
        while True:
            user_input = client_socket[1].recv(MAX_PACKET).decode().upper()
            match user_input:
                # TIME - sends back the current time #
                case 'TIME':
                    client_socket[1].send(protocol_format(Commands.comm_time()).encode())

                # NAME - sends back the name of the command prompt #
                case 'NAME':
                    client_socket[1].send(protocol_format(Commands.comm_name()).encode())

                # RAND - sends back a random number between 1 & 10 #
                case 'RAND':
                    client_socket[1].send(protocol_format(str(Commands.comm_rand())).encode())

                # EXIT - disconnects the client from the server #
                case 'EXIT':
                    Commands.comm_exit(client_socket[1])
                    print(f"client disconnected: {client_socket[0]}")
                    break

                case _:
                    logging.info(f"Client '{client_socket[0]}' Crashed")


def client_handle(socket: sock.socket):
    """
    handling the client input and connection
    :param socket: the client socket
    :return None:
    """
    # waiting for client connection & getting client info #
    socket.listen(QUEUE_LEN)
    while True:
        client_socket, client_ip = socket.accept()
        print(f"client connected: {client_ip}")

        # Sending the command list #
        client_socket.send(f"{Commands.commands=}".encode())

        try:
            Commands.command_validate_and_run((client_ip, client_socket))

        except Exception as err:
            logging.exception(err)

        finally:
            client_socket.close()


# Main Server Code #
def main() -> None:
    # socket creation #
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    # handling client #
    try:
        # Connecting to the socket #
        socket.bind((IP, PORT))

        # Client Handle #
        client_handle(socket)

    except sock.error as err:
        logging.exception(err)

    finally:
        socket.close()


if __name__ == '__main__':
    # Logging handling #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # Auto Checks #
    assert Commands.comm_name() == SERVER_NAME, ERR_SERVER_NAME_ASSERTION
    assert 11 > Commands.comm_rand() > 0, ERR_RAND_ASSERTION
    assert protocol_format("msg") == PROTOCOL_FORMAT.format(msg_len=str(len("msg")), msg="msg"), ERR_PROTOCOL_ASSERTION

    # Running main code #
    main()
