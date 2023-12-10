"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/12/2023
    DESCRIPTION: All of the functions needed for the server
"""
# Imports #
import logging
import os
import glob
import pyautogui
import socket as sock

import protocol
from server import Server
from typing import List

# Constants #
ERR_FOLDER_NOT_FOUND = "False Folder not found"
ERR_FILE_NOT_FOUND = "False File not found"

SUCC_FILE_REMOVE = "True File removed"

# TODO: finish all of the commands
def exit_client(client_socket: sock.socket, server: Server) -> None:
    """
    Disconnects the client
    :return: None
    """
    server.send_message(client_socket, "True Disconnecting...")
    client_socket.close()

def take_screenshot() -> str:
    """
    Takes a screenshot and sends to the client
    :return: the file bytes / error message
    """
    image = pyautogui.screenshot()
    image.save(r'screen.jpg')

    try:
        with open('screen.jpg', 'rb') as f:
            return "True " + str(f.read())
    except FileNotFoundError:
        return ERR_FILE_NOT_FOUND
    except Exception as err:
        logging.exception(err)
        return "False " + str(err)


def execute():
    pass


def dir_contents(path) -> List[str]:
    """
    Returns the contents of a folder
    :param path: the folder path
    :return List[str]: Folder content
    """
    if not os.path.isdir(path):
        logging.info(ERR_FOLDER_NOT_FOUND)
        return [ERR_FOLDER_NOT_FOUND]

    folder_content = glob.glob(path+"\\*.*")
    return "True " + path + ":" + "".join([f'\n\t{i}' for i in folder_content] if folder_content != [] else "Null")


def copy():
    pass


def delete(file_path) -> str:
    """
    deletes a file according to the given path
    :param file_path: the file path
    :return: success\fail message
    """
    try:
        os.remove(file_path)
        return SUCC_FILE_REMOVE
    except FileNotFoundError:
        logging.error(ERR_FILE_NOT_FOUND)
        return ERR_FILE_NOT_FOUND
    except Exception as err:
        logging.exception(err)
        return "False " + str(err)
