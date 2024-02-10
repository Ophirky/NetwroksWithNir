"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 26/01/24
    DESCRIPTION: Simple UDP server
"""
# Imports #
import logging
import socket as sock

# Constants #
PORT = 5500
IP = "127.0.0.1"
QUEUE_LENGTH = 1
MAX_PACKET = 1024


def main() -> None:
    """
    the main function
    :return: None
    """
    socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

    try:
        socket.bind((IP, PORT))
        data = b''
        while data != b"quit":
            data, client_ip = socket.recvfrom(MAX_PACKET)
            print(data)
            socket.sendto(b"message received", client_ip)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
