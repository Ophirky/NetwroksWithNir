"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/12/2023
    DESCRIPTION: the functions for the client
"""
# Imports #
import os
import base64
import binascii
from PIL import Image
from io import BytesIO
import logging

# Constants #
COMMANDS = ("DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "EXIT")

def save_image_to_file(image_data) -> None:
    """
    saves the image from the raw byte data to a file
    :param image_data: The string with the image data
    :return: None
    """

    try:
        decoded_image = base64.b64decode(image_data)

        image = Image.open(BytesIO(decoded_image))
        image.save('received_image.jpg', 'jpeg')
        image.show()
    except binascii.Error:
        logging.error('Error while trying to decode image')
        print('Error decoding image')

def validate_msg(msg: str) -> bool:
    """
    Check if the msg is a command
    :param msg: the msg from the user
    :return bool: Whether the msg is valid or not
    """
    return any(msg.startswith(i) for i in COMMANDS)
