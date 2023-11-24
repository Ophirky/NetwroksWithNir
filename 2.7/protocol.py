"""
    AUHTOR: Ophir Nevo Michrowski
    DESCRIPTION:This file is the protocol formatting library
                protocol formatting = "len|comm/was_successful|payload"
    DATE: 24/11/23
"""

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

print(format_message("COPY c:\\hukana\\matata c:\\banana").decode())
