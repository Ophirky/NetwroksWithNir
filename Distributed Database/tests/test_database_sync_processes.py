"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Testing the processes not in a unittests because they do not work well together
"""
import multiprocessing
import time
from operation_methods import OperationSettings
from database_syncer import DbSynchronizer
from tests.log_manager import LOGGER
from typing import Any


class DbSynchronizerTests:
    def __init__(self):
        self.db_sync = multiprocessing.Manager().SharedDatabase = DbSynchronizer(
            operation_method=OperationSettings.PROCESSES, name="test_processes")

        self.tmp_db = multiprocessing.Manager().SharedDatabase = DbSynchronizer(OperationSettings.PROCESSES,
                                                                                'tmp_db_processes')
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
        LOGGER.debug('No contest reading test complete')

    def test_write_then_read(self) -> None:
        """Test trying to read while a writer is writing."""
        key, val = "age", "17"

        p1 = multiprocessing.Process(target=self.write, args=(key, val, self.db_sync, "write then read"))
        p2 = multiprocessing.Process(target=self.read, args=(key, val, self.db_sync, "write then read"))

        p1.start()
        time.sleep(.1)
        p2.start()
        for p in [p1, p2]:
            p.join()

    def test_read_then_write(self) -> None:
        """Test trying to read while a writer is writing."""
        key, val = "height", "tall"

        p1 = multiprocessing.Process(target=self.read, args=(key, None, self.db_sync, "read then write"))
        p2 = multiprocessing.Process(target=self.write, args=(key, val, self.db_sync, "read then write"))

        p1.start()
        time.sleep(0.1)  # Ensure the read starts first
        p2.start()

        p1.join()
        p2.join()

    def test_multiple_readers(self) -> None:
        """Test multiple readers at the same time."""
        self.db_sync.write_to_db(self.key, self.value)
        processes = [
            multiprocessing.Process(target=self.read, args=(self.key, self.value, self.db_sync, "multiple readers"))
            for _ in range(10)
        ]

        for p in processes:
            p.start()
        for p in processes:
            p.join()

    def test_final(self) -> None:
        """Final test with a different database instance."""
        processes = [multiprocessing.Process(target=self.read, args=("num", None, self.tmp_db, "final")) for _
                     in range(3)]
        writing_process = multiprocessing.Process(target=self.write, args=("num", "12", self.tmp_db, "final"))
        processes2 = [multiprocessing.Process(target=self.read, args=("num", "12", self.tmp_db, "final")) for
                      _ in range(3)]

        for p in processes:
            p.start()
        time.sleep(0.001)
        writing_process.start()
        time.sleep(0.001)

        for p in processes2:
            p.start()

        for p in processes + processes2 + [writing_process]:
            p.join()

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
