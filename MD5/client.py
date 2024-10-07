"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: MD5 bruteforce decryption client program.
"""
import socket
import hashlib
import threading
import os
import logging as log

import protocol

# Client configurations #
SERVER_IP = '127.0.0.1'  # Server address
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Socket setup #
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5)

LOG_LEVEL = log.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\client_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

# Global variables #
found_result = None
result_lock = threading.Lock()
stop_event = threading.Event()


def send(msg: bytes):
    """
    Sends a message to the server #
    :param msg: the msg to send in bytes
    :return: None
    """
    client_socket.sendall(msg)


def generate_md5_hash(num):
    """
    takes a number and encrypts it in the md5 hash function
    :param num: the number to encrypt
    :return: the encrypted cipher
    """
    return hashlib.md5(str(num).encode()).hexdigest()


def brute_force(target_hash, start, end):
    """
    brute forces the given range to the numbers
    :param target_hash: the target hash to decipher
    :param start: the start of the range
    :param end: the end of the range
    :return: none
    """
    global found_result

    for number in range(start, end + 1):
        if stop_event.is_set():
            return  # Exit if stop signal received

        if generate_md5_hash(number) == target_hash:
            with result_lock:
                if found_result is None:  # Check if another thread has already found the result
                    found_result = number
            stop_event.set()  # Set the event to stop all threads
            return


def main():
    """
    The main function
    :return: None
    """
    global found_result

    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))

    # Request a range from the server #
    send(b"request")

    while True:
        try:
            # Try and get a msg from the server #
            data = client_socket.recv(BUFFER_SIZE)
            message = data.decode()

        # If server shut down #
        except ConnectionAbortedError:
            break

        # If server sends stop message #
        if message == protocol.MD5DecryptionProtocol.stop().decode():
            log.debug("Stop signal received, halting operations.")
            stop_event.set()
            break

        range_part, target_hash = message.split(',')
        start, end = map(int, range_part.split('-'))

        log.debug(f"Received range {start}-{end}, target hash {target_hash}")

        # Set number of threads on number of logical processors #
        num_threads = os.cpu_count()
        chunk_size = (end - start + 1) // num_threads
        threads = []

        # Create and start threads
        for i in range(num_threads):
            thread_start = start + i * chunk_size
            thread_end = start + (i + 1) * chunk_size - 1 if i < num_threads - 1 else end

            thread = threading.Thread(target=brute_force, args=(target_hash, thread_start, thread_end))
            threads.append(thread)
            thread.start()

        # Wait for threads to finish #
        for thread in threads:
            thread.join()

        if found_result is not None:
            log.debug(f"Found match: {found_result}")
            send(protocol.MD5DecryptionProtocol.found(found_result))
            break
        else:
            send(protocol.MD5DecryptionProtocol.request())

    client_socket.close()


if __name__ == "__main__":
    # Setting up logger #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    log.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format=LOG_FORMAT)

    # Calling main function #
    main()
