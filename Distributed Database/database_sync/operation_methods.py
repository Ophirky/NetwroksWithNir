"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Db Operation Methods
"""
from enum import Enum


class OperationSettings(Enum):
    """Operation settings for the project"""

    THREADS = 0
    PROCESSES = 1
