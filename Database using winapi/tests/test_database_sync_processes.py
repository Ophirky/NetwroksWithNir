"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Testing the processes not in an unittests because they do not work well together
"""
import win32process
import win32event
import time
from database_syncer import DbSynchronizer
from tests.log_manager import LOGGER
from typing import Any

# Constants #
INFINITE = -1


class DbSynchronizerTests:
    def __init__(self):
        self.db_sync = DbSynchronizer("test_processes")
        self.tmp_db = DbSynchronizer('tmp_db_processes')
        self.key, self.value = "name", "Ophir"

    @staticmethod
    def read(key: Any, expected_result: Any, db: DbSynchronizer, test_name: str) -> None:
        """
        Read from db and test result.
        :param test_name: the test name for the logs
        :param db: the db to read from
        :param key: the key to read from the db.
        :param expected_result: the expected result.
        :return: None
        """
        result = db.read_from_db(key)
        if result != expected_result:
            raise AssertionError(f"Test {test_name} failed: Expected {expected_result}, got {result}")
        LOGGER.debug('Finished reading - ' + test_name)

    @staticmethod
    def write(key: Any, value: Any, db: DbSynchronizer, test_name: str) -> None:
        """
        Write to db and test result.
        :param test_name: the test name for the logs
        :param db: the db to write to
        :param key: the key to write to the db.
        :param value: the value to write.
        :return: None
        """
        result = db.write_to_db(key, value)
        if not result:
            raise AssertionError(f"Test {test_name} failed: Write operation was not successful")
        LOGGER.debug('Finished writing - ' + test_name)

    def create_process(self, target, args):
        """Utility function to create a process using pywin32's CreateProcess."""
        command = f"python -c \"import sys; from __main__ import {target}; {target}(*{args})\""
        startup_info = win32process.STARTUPINFO()
        process_info = win32process.CreateProcess(
            None,  # Application name
            command,  # Command line
            None,  # Process attributes
            None,  # Thread attributes
            False,  # Inherit handles
            win32process.CREATE_NO_WINDOW,  # Creation flags
            None,  # Environment
            None,  # Current directory
            startup_info  # Startup Info
        )
        return process_info

    def test_no_contest_write(self) -> None:
        """Test writing to the database without any contention."""
        result = self.db_sync.write_to_db(self.key, self.value)
        if not result:
            raise AssertionError("Test 'no contest write' failed: Write operation was not successful")
        LOGGER.debug('No contest writing test finished')

    def test_no_contest_read(self) -> None:
        """Test reading from the database without any contention."""
        result = self.db_sync.read_from_db(self.key)
        if result != self.value:
            raise AssertionError(f"Test 'no contest read' failed: Expected {self.value}, got {result}")
        LOGGER.debug('No contest reading test complete, ' + result)

    def test_write_then_read(self) -> None:
        """Test trying to read while a writer is writing."""
        key, val = "age", "17"

        p1 = self.create_process("DbSynchronizerTests.write", (key, val, self.db_sync, "write then read"))
        p2 = self.create_process("DbSynchronizerTests.read", (key, val, self.db_sync, "write then read"))

        win32event.WaitForSingleObject(p1[0], INFINITE)
        time.sleep(0.1)
        win32event.WaitForSingleObject(p2[0], INFINITE)

    def test_read_then_write(self) -> None:
        """Test trying to read while a writer is writing."""
        key, val = "height", "tall"

        p1 = self.create_process("DbSynchronizerTests.read", (key, None, self.db_sync, "read then write"))
        p2 = self.create_process("DbSynchronizerTests.write", (key, val, self.db_sync, "read then write"))

        win32event.WaitForSingleObject(p1[0], INFINITE)
        time.sleep(0.1)
        win32event.WaitForSingleObject(p2[0], INFINITE)

    def test_multiple_readers(self) -> None:
        """Test multiple readers at the same time."""
        self.db_sync.write_to_db(self.key, self.value)
        processes = [
            self.create_process("DbSynchronizerTests.read", (self.key, self.value, self.db_sync, "multiple readers"))
            for _ in range(10)
        ]

        for p in processes:
            win32event.WaitForSingleObject(p[0], INFINITE)

    def test_final(self) -> None:
        """Final test with a different database instance."""
        processes = [self.create_process("DbSynchronizerTests.read", ("num", None, self.tmp_db, "final")) for _ in
                     range(3)]
        writing_process = self.create_process("DbSynchronizerTests.write", ("num", "12", self.tmp_db, "final"))
        processes2 = [self.create_process("DbSynchronizerTests.read", ("num", "12", self.tmp_db, "final")) for _ in
                      range(3)]

        for p in processes:
            win32event.WaitForSingleObject(p[0], INFINITE)
        time.sleep(0.001)
        win32event.WaitForSingleObject(writing_process[0], INFINITE)
        time.sleep(0.001)

        for p in processes2:
            win32event.WaitForSingleObject(p[0], INFINITE)

    def run_tests(self) -> None:
        """Run all tests and report results."""
        try:
            self.test_no_contest_write()
            self.test_no_contest_read()
            self.test_write_then_read()
            self.test_read_then_write()
            self.test_multiple_readers()
            self.test_final()
            print("All tests passed successfully.")
        except AssertionError as e:
            print(str(e))
