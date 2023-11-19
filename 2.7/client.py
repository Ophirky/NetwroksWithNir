"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Remote server interaction interface
"""
# Imports #
import socket


# Client class #
class Client:
    """
    Client class for interacting with the server.
    """

    def __init__(self, host, port):
        """
        Initialize the client object with host and port information.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The port number of the server.
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

    def connect(self):
        """
        Connect to the server.
        """
        self.sock.connect((self.host, self.port))  # Establish a connection to the server

    # TODO: add protocol format
    def send_command(self, command, args=""):
        """
        Send a command to the server.

        Args:
            command (str): The command to send.
            args (str, optional): The arguments to send with the command.
                Defaults to an empty string.
        """
        message = "%d|%s|%s" % (len(command + args) + 3, command, args)  # Format the command message
        self.sock.sendall(message.encode())  # Send the formatted command message to the server

    # TODO: add protocol deformat
    def receive_response(self):
        """
        Receive a response from the server.

        Returns:
            tuple: A tuple of three values:
                - length (int): The length of the response message.
                - was_successful (bool): Whether the command was successful.
                - message (str): The server's response message.
        """
        response = self.sock.recv(1024).decode()  # Receive the response message from the server
        length, was_successful, message = response.split("|")  # Parse the response message
        return int(length), bool(was_successful), message  # Return the parsed response data
