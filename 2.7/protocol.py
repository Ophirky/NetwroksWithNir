"""
    AUHTOR: Ophir Nevo Michrowski
    DESCRIPTION:This file is the protocol formatting library
                protocol formatting = "len|comm/was_successful|payload"
    DATE: 24/11/23
"""

# Imports #
import socket as sock
from typing import Tuple

def format_message(msg: str) -> bytes:
    """
    formats message to the protocol from the client to the server
    :param msg: the command used by the client
    :return: bytes formatted to the protocol
    """

    # msg formatting #
    msg = msg.split(" ", 1)
    protocol = f"{msg[0]}|{msg[1]}"  # msg[0] -> command\was_successful, msg[1] -> payload

    # Add the msg len #
    protocol = str(len(protocol)) + "|" + protocol

    # Return the byte code for the protocol #
    return protocol.encode()


def deformat_message(socket: sock.socket) -> Tuple:
    """
    Accepts the message and deformats it
    :param socket: the socket that is used in the program
    :return: tuple -> (comm/was_successful, payload)
    """
    # Getting the length of the message #
    length = 0
    char = socket.recv(1).decode()
    while char != '|':
        length = (length * 10) + int(char)
        char = socket.recv(1).decode()


    return tuple(socket.recv(length).split(b'|'))

