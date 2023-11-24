"""
    AUHTOR: Ophir Nevo Michrowski
    DESCRIPTION:This file is the protocol formatting library
                protocol formatting = "len|comm/was_successful|payload"
    DATE: 24/11/23
"""

# Imports #
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

# TODO: Write the deformat_message function (also accepts the message)
def deformat_message(fmsg: bytes) -> Tuple:
    """
    Accepts the message and deformats it
    :param fmsg: the formatted message
    :return: tuple -> (comm/was_successful, payload)
    """
    pass
