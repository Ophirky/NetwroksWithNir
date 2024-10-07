"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Protocol class
"""


class MD5DecryptionProtocol:
    found_start = "found:"

    @staticmethod
    def range(start, end, target):
        """
        generate a protocol based msg
        :param start: start of range
        :param end: end of range
        :param target: the cipher to decipher
        :return: bytes
        """
        return f'{start}-{end},{target}'.encode()

    @staticmethod
    def stop():
        """
        will generate the stop msg
        :return: bytes
        """
        return b'stop'

    @staticmethod
    def request():
        """
        will generate the request msg
        :return: bytes
        """
        return b'request'

    @staticmethod
    def found(num):
        """
        generates the found msg
        :param num: the result
        :return: bytes
        """
        return f"found:{num}".encode()
