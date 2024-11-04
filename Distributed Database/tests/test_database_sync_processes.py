import unittest
import multiprocessing
import time

from operation_methods import OperationSettings
from database_syncer import DbSynchronizer
from log_manager import LOGGER
from typing import Any

db_sync = DbSynchronizer(operation_method=OperationSettings.PROCESSES, name="test_processes")
tmp_db = DbSynchronizer(OperationSettings.PROCESSES, 'tmp_db_processes')


class TestDbSynchronizerWithProcesses(unittest.TestCase):
    key, value = "name", "Ophir"

    def read(self, key: Any, result: Any, db: DbSynchronizer, test: str) -> None:
        """
        Read from db and test result.
        :param test: the test name for the logs
        :param db: the db to read from
        :param key: the key to read from the db.
        :param result: the expected result.
        :return: None
        """
        res = db.read_from_db(key)

        self.assertEqual(res, result)
        LOGGER.debug('finished reading - ' + test)

    def write(self, key: Any, value: Any, db: DbSynchronizer, test: str) -> None:
        """
        Write to db and test result
        :param test: the test name for the logs
        :param db: the db to write to
        :param key: the key to write to  the db.
        :param value: the value to write.
        :return: None
        """
        res = db.write_to_db(key, value)

        self.assertTrue(res)
        LOGGER.debug('finished writing - ' + test)

    def test_no_contest_write(self) -> None:
        """
        Test writing to the file using processes without any contest
        :return: None
        """
        res = db_sync.write_to_db(self.key, self.value)

        self.assertTrue(res)
        LOGGER.debug('no contest writing test finished')

    def test_no_contest_read(self) -> None:
        """
        Test writing to the file using processes without any contest
        :return: None
        """
        # Making sure that it is written
        db_sync.write_to_db(self.key, self.value)

        res = db_sync.read_from_db(self.key)
        self.assertEqual(self.value, res)
        LOGGER.debug('no contest reading test complete')

    def test_write_then_read(self) -> None:
        """
        Test trying to read while writer is writing.
        :return: None
        """
        key, value = "age", 17

        processes = [multiprocessing.Process(target=self.write, args=[key, value, db_sync, "write then read"]),
                     multiprocessing.Process(target=self.read, args=[key, value, db_sync, "write then read"])]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

    def test_read_then_write(self) -> None:
        """
        Test trying to read while writer is writing.
        :return: None
        """
        key, value = "height", "tall"

        p1 = multiprocessing.Process(target=self.read, args=[key, None, db_sync, "read then write"])
        p2 = multiprocessing.Process(target=self.write, args=[key, value, db_sync, "read then write"])

        p1.start()
        time.sleep(.1)
        p2.start()

        p1.join()
        p2.join()

    def test_multiple_readers(self) -> None:
        """
        Test multiple readers at the same time
        :return: None
        """
        db_sync.write_to_db(self.key, self.value)

        processes = [multiprocessing.Process(target=self.read, args=[self.key, self.value, db_sync,
                                                                     "multiple readers"]) for i in range(10)]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

    def test_final(self) -> None:
        """
        Test in different db!
        Final Test
        :return: None
        """

        processes = [multiprocessing.Process(target=self.read, args=["num", None, tmp_db, "write then read"])
                     for i in range(3)]

        writing_process = multiprocessing.Process(target=self.write, args=["num", "12", tmp_db, "write then read"])

        processes2 = [multiprocessing.Process(target=self.read, args=["num", "12", tmp_db, "write then read"])
                      for i in range(3)]

        for p in processes:
            p.start()

        time.sleep(.001)
        writing_process.start()
        time.sleep(.001)

        for p in processes2:
            p.start()

        for p in processes + processes2 + [writing_process]:
            p.join()
