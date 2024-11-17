import win32file
import pywintypes


def check_file_exists() -> bool:
    """
    Check if file exists
    :return: Whether the file exists or not
    """
    # Try to open file #
    res = False
    try:
        file_handle = win32file.CreateFile(
            "database.py",
            win32file.GENERIC_READ,
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None
        )

        print(win32file.GetFileSize(file_handle))
        win32file.CloseHandle(file_handle)
        res = True
    except pywintypes.error as e:
        if e.winerror != 2:
            raise

    return res

print(check_file_exists())
