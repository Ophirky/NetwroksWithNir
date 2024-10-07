"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: MD5 Decryption and management server.
"""
import socket
import threading
import logging as log
import os

import protocol

# Server settings #
SERVER_ADDRESS = ('localhost', 12345)
BUFFER_SIZE = 1024
MAX_NUMBER = 9999999999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Global variables #
CIPHER = '283f42764da6dba2522412916b031080'
start_range = 0
CHUNK_SIZE = 100000

LOG_LEVEL = log.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\server_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

clients = {}
active_clients = {}
lock = threading.Lock()
answer_found = threading.Event()


# send function #
def send(sock: socket.socket, msg: bytes):
    """
    Sends a msg to a client
    :param sock: the socket to send to
    :param msg: the msg
    :return: None
    """
    sock.sendall(msg)


# Handle client connection #
def handle_client(client_socket, client_address):
    """
    Handles the client connection
    :param client_socket: the client socket
    :param client_address: the client ip address
    :return: None
    """
    global answer_found, CHUNK_SIZE, start_range

    while not answer_found.is_set():
        with lock:
            # If there is no answer or out of range #
            if start_range >= MAX_NUMBER and not answer_found.is_set():
                stop_all_clients()
                print("No Answer Found")
                answer_found.set()
                break

            elif start_range >= MAX_NUMBER and answer_found.is_set():
                stop_all_clients()
                break

            # Assign a range to the client #
            end_range = min(start_range + CHUNK_SIZE, MAX_NUMBER)
            chunk = protocol.MD5DecryptionProtocol.range(start_range, end_range, CIPHER)
            start_range += CHUNK_SIZE

        send(client_socket, chunk)

        # Response #
        try:
            data = client_socket.recv(BUFFER_SIZE)
            message = data.decode()

            # Answer found #
            if message.startswith(protocol.MD5DecryptionProtocol.found_start):
                print(f"Client {client_address} found the solution: {message}")
                with lock:
                    answer_found.set()
                    stop_all_clients()
                break
            else:
                log.debug(f"Client {client_address} didn't find a match, continuing...")

        except ConnectionResetError:
            log.debug(f"Connection with {client_address} was reset. Stopping thread.")
            break

    log.debug(f"Closing connection with {client_address}")
    client_socket.close()  # Close the client socket
    del clients[client_address]  # Clean up client on disconnection


# Stop all clients by sending a stop message #
def stop_all_clients():
    """
    Sends a stop message to all the clients
    :return: None
    """
    global server_socket
    for client in active_clients.keys():
        # Send the answer_found message to all active clients
        send(client, protocol.MD5DecryptionProtocol.stop())
    log.debug("All clients have been notified to answer_found.")


# Main function #
def main():
    """
    The main function
    :return: None
    """
    global answer_found
    global server_socket

    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()
    server_socket.settimeout(10)
    log.debug(f"Server listening on {SERVER_ADDRESS}")

    while not answer_found.is_set():
        try:
            client_socket, client_address = server_socket.accept()
            if client_address not in clients:
                # Create a new thread only if this client doesn't have one #
                log.debug(f"New client connected: {client_address}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                clients[client_address] = client_thread
                active_clients[client_socket] = True
                client_thread.start()
            else:
                log.debug(f"Client {client_address} is already connected and active.")

        except socket.timeout:
            log.debug("no new client")

        except Exception as e:
            log.debug(f"Server error: {e}")
            break

    # Closing server #
    server_socket.close()
    log.debug("Server has shut down.")


# Calling main function #
if __name__ == "__main__":
    # Setting up logger #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    log.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format=LOG_FORMAT)

    # Calling main function #
    main()
