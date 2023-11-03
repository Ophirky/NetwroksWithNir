"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/2/2023
    DESCRIPTION: simple remote command line server.
"""
# Imports #
import socket as sock
import random as ran
import datetime as dt
from typing import List, Dict

# Constants #
IP = "0.0.0.0"
PORT = 5500
MAX_PACKET = 1024
QUEUE_LEN = 1


# Commands Class #
class Commands:
    commands = {
        "TIME": "Sends the time",
        "WHORU": "Sends the command lines name",
        "RAND": "rolls a d6 dice",
        "EXIT": "closes the server"
    }

    def get_commands(self) -> Dict:
        """
        :return dict: returns a dictionary of all the commands
        """
        return self.commands

    @staticmethod
    def comm_time() -> str:
        """
        :return str: returns the current time
        """
        return dt.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def comm_whoru() -> str:
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
        :return:
        """
        client_socket.close()

# Server Class #
class Server:
    pass

# Main Server Code #
def main() -> None:
    running = True
    while running:
        comm = input("Enter a command")

        match comm:
            case 'TIME':
                print(Commands.comm_time())

if __name__ == '__main__':
    main()