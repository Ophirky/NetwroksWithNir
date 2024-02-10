"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/02/24
"""

# Imports #
from scapy.all import *

def send_message(message) -> None:
    """
    Handles the message sending and formatting
    :param message: The message to send
    :return: None
    """
    server_ip = input("Enter the server ip: ")
    for char in message:
        ascii_value = ord(char)
        packet = IP(dst=server_ip) / UDP(dport=ascii_value)
        send(packet)

def main() -> None:
    """
    the Main function
    :return: None
    """
    message = input("Enter msg: ")
    send_message(message)
    print("Msg sent!")


if __name__ == '__main__':
    main()
