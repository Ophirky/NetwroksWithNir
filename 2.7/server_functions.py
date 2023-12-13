"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/12/2023
    DESCRIPTION: All of the functions needed for the server
"""
# Imports #
import logging
import os
import glob
import shutil
import subprocess
from PIL import ImageGrab
import base64
import socket as sock
from typing import List

# Constants #
ERR_FOLDER_NOT_FOUND = "False Folder not found"
ERR_FILE_NOT_FOUND = "False File not found"
ERR_PROGRAM_FAILED_TO_RUN = "False Failed to run the requested program"

SUCC_FILE_REMOVE = "True File removed"
SUCC_FILE_COPY = "True File copy was a success"
SUCC_EXECUTE_PROGRAM = "True Program is running"

# TODO: finish all of the commands
def exit_client(client_socket: sock.socket) -> None:
    """
    Disconnects the client
    :param client_socket: the socket to close
    :return: None
    """
    client_socket.close()

def take_screenshot() -> str:
    """
    Takes a screenshot and sends to the client
    :return: the file bytes / error message
    """
    ret: str

    try:
        ImageGrab.grab(all_screens=True).save('screenshot.jpg')
        with open('screenshot.jpg', 'rb') as f:
            ret_val = "True " + base64.b64encode(f.read()).decode('utf-8')
        os.remove('screenshot.jpg')

    except Exception as err:
        logging.exception(err)
        ret_val = "False " + str(err)

    return ret_val


def execute(program_path) -> str:
    """
    Executes a requested program
    :param program_path: the path to the .exe file
    :return str: the success\fail msg
    """
    try:
        subprocess.call(program_path)
        return SUCC_EXECUTE_PROGRAM
    except Exception as err:
        logging.exception(err)
        return ERR_PROGRAM_FAILED_TO_RUN


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


def copy(file_to_copy_from_path, file_to_copy_to_path) -> str:
    """
    copies one file to another
    :param file_to_copy_from_path: the file path to the file to copy from
    :param file_to_copy_to_path: the file path to the destination file
    :return: str success/fail msg
    """
    try:
        shutil.copy(file_to_copy_from_path, file_to_copy_to_path)
        return SUCC_FILE_COPY
    except FileNotFoundError:
        return ERR_FILE_NOT_FOUND
    except shutil.Error as err:
        logging.error(err)
        return "False " + str(err)
    except Exception as err:
        logging.exception(err)
        return "False " + str(err)

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
