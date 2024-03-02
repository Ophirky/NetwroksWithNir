"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 25/02/2024
    DESC: Check what ports are open on a pc
"""
# Imports #
from scapy.all import *
import sys
import os
import logging

# Constants #
RST_ACK_FLAG = 0x14
SYN_ACK_FLAG = 0x12

START_PORT = 20
END_PORT = 1024
TIMEOUT = 0.5

LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\server_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

# Validate Ip #
def validate_ip(ip: str) -> bool:
    """
    checks if a given ip is valid
    :param ip: the ip to validate
    :return bool: whether the ip is valid or not
    """
    parts = ip.split(".")
    if len(parts) != 4:
        logging.warning(f"Invalid IP address format: {ip}")
        return False
    for part in parts:
        if not part.isdigit():
            logging.warning(f"IP address part is not a number: {part} in {ip}")
            return False
        num = int(part)
        if num < 0 or num > 255:
            logging.warning(f"IP address part out of range: {num} in {ip}")
            return False
    logging.info(f"IP address validated: {ip}")
    return True


# Check if a port is open #
def scan_port(ip: str, port: int) -> bool:
    """
    scans a specific port
    :param ip: the ip of the pc to check
    :param port: the port to check
    :return bool: whether the port is open or not
    """

    resp = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=TIMEOUT, verbose=0)
    
    # Check Response #
    if resp is None:
        logging.debug(f"No response received for port {port}.")
        return False
    elif resp.haslayer(TCP):
        # Is port open #
        if resp.getlayer(TCP).flags == SYN_ACK_FLAG:
            sr(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=TIMEOUT, verbose=0) # close the connection with the open port
            logging.info(f"Port {port} is open.")
            return True
        # Is port closed #
        elif resp.getlayer(TCP).flags == RST_ACK_FLAG:
            logging.debug(f"Port {port} is closed.")
            return False


# Main #
def main() -> None:
    """
    The main function of the program
    :return None:
    """

    # User input #
    target_ip = input("Enter the target ip: ")

    if not validate_ip(target_ip):
        logging.error("IP validation failed.")
        return

    logging.info(f"Scanning {target_ip} for open ports...")
    
    # Scan for the ports #
    for port in range(START_PORT, END_PORT + 1):
        if scan_port(target_ip, port):
            print(f"Port {port} is open!")
        else:
            print(f"Port {port} is closed")
            logging.debug(f"Port {port} checked and found closed.")

    
if __name__ == "__main__":
    # Asserts #
    assert isinstance(START_PORT, int) and START_PORT > 0, "START_PORT must be a positive integer."
    assert isinstance(END_PORT, int) and END_PORT >= START_PORT, "END_PORT must be greater than or equal to START_PORT."
    assert isinstance(TIMEOUT, (int, float)) and TIMEOUT > 0, "TIMEOUT must be a positive number."

    # Log setup #
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format=LOG_FORMAT)

    # Main function call #
    main()
