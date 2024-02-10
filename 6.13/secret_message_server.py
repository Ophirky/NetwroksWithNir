"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/02/24
"""

from scapy.all import *


def is_empty_packet(packet) -> bool:
    """
    Checks if a packet has an empty payload.
    :param packet: the UDP packet to check
    :return: True if packet is empty else False
    """
    res = False
    payload = packet[UDP].payload
    if isinstance(payload, Padding) and payload.load == b'\x00' * len(payload.load):
        return True
    return res


def sniff_packets(packet) -> None:
    """
    Turns the packets sent to the message
    :param packet: the UDP packet to decode
    :return: None
    """
    if packet.haslayer(UDP) and is_empty_packet(packet):
        port = packet.dport
        char = chr(port)
        print(char, end="")


def main() -> None:
    """
    the main function
    :return: None
    """
    sniff(prn=sniff_packets)


if __name__ == '__main__':
    # Asserts
    sample_packet_not_empty = IP(dst="0.0.0.0") / UDP(dport=34) / Raw(b"hello")

    # assert is_empty_packet(sample_packet_empty)
    assert not is_empty_packet(sample_packet_not_empty)

    # The main call
    main()
