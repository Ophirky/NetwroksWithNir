"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/11/2023
    DESCRIPTION: Server technician interaction app
"""
# Imports #
import socket


# Command handling #

class Commands:
    # Commands #
    @staticmethod
    def exit():
        pass

    @staticmethod
    def take_screenshot():
        pass

    @staticmethod
    def execute():
        pass

    @staticmethod
    def dir():
        pass

    @staticmethod
    def copy():
        pass

    @staticmethod
    def delete():
        pass

    # Command handling #
    @staticmethod
    def handle_command(client, command, args):
        """
        Handle a command received from a client.

        Args:
            client (Client): The client object representing the connected client.
            command (str): The command received from the client.
            args (str): The arguments received with the command from the client.
        """
        if command == "COPY":
            try:
                shutil.copy(args[0], args[1])  # Execute the COPY command
                response = "File copied successfully"  # Prepare a success response
                was_successful = True  # Set success flag
            except Exception as e:  # Handle any errors during command execution
                response = "Error copying file: %s" % e  # Prepare an error response
                was_successful = False  # Set failure flag

        elif command == "TAKE_SCREENSHOT":
            try:
                screenshot = pyscreenshot.grab()  # Take a screenshot using pyscreenshot
                screenshot.save('screenshot.png')  # Save the screenshot to a file
                response = "Screenshot taken successfully"  # Prepare a success response
                was_successful = True  # Set success flag
            except Exception as e:  # Handle any errors during screenshot capture
                response = "Error taking screenshot: %s" % e  # Prepare an error response

class Server:
    """
    Server class for handling client connections.
    """

    def __init__(self, host, port, queue_len):
        """
        Initialize the server object with host and port information.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The port number of the server.
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.sock.bind((self.host, self.port))  # Bind the socket to the specified host and port
        self.sock.listen(queue_len)  # Listen for incoming connections

    def accept_connection(self):
        """
        Accept a connection from a client.

        Returns:
            Client: A new Client object representing the connected client.
        """
        client_sock, client_addr = self.sock.accept()  # Accept an incoming connection from a client
        return Client(client_addr[0], client_addr[1])  # Create a Client object for the connected client

