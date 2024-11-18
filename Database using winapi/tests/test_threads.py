import unittest
import threading
import time

from database_syncer import DbSynchronizer
from tests.log_manager import LOGGER
from typing import Any


class DbSynchronizerTests(unittest.TestCase):
    db_sync = DbSynchronizer(name="test_threads")
    key, value = "name", "Ophir"

    def test_no_contest_write(self) -> None:
        """
        Test writing to the file using threads without any contest
        :return: None
        """
        res = self.db_sync.write_to_db(self.key, self.value)

        self.assertTrue(res)
        LOGGER.debug('no contest writing test finished')

    def test_no_contest_read(self) -> None:
        """
        Test writing to the file using threads without any contest
        :return: None
        """
        # Making sure that it is written
        self.db_sync.write_to_db(self.key, self.value)

        res = self.db_sync.read_from_db(self.key)
        self.assertEqual(self.value, res)
        LOGGER.debug('no contest reading test complete')

    def test_write_then_read(self) -> None:
        """
        Test trying to read while writer is writing.
        :return: None
        """
        key, value = "age", 17

        def read() -> None:
            """
            Read from db and test result
            :return: None
            """
            res = self.db_sync.read_from_db(key)

            self.assertEqual(res, value)
            LOGGER.debug('finished reading - write then read')

        def write() -> None:
            """
            Write to db and test result
            :return: None
            """
            res = self.db_sync.write_to_db(key, value)

            self.assertTrue(res)
            LOGGER.debug('finished writing - write then read')

        threads = [threading.Thread(target=write),
                   threading.Thread(target=read)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def test_read_then_write(self) -> None:
        """
        Test trying to read while writer is writing.
        :return: None
        """
        key, value = "height", "tall"

        def read() -> None:
            """
            Read from db and test result
            :return: None
            """
            res = self.db_sync.read_from_db(key)

            self.assertEqual(res, None)
            LOGGER.debug('finished reading - read then write')

        def write() -> None:
            """
            Write to db and test result
            :return: None
            """
            res = self.db_sync.write_to_db(key, value)

            self.assertTrue(res)
            LOGGER.debug('finished writing - read then write')

        t1 = threading.Thread(target=read)
        t2 = threading.Thread(target=write)

        t1.start()
        time.sleep(.1)
        t2.start()

        t1.join()
        t2.join()

    def test_multiple_readers(self) -> None:
        """
        Test multiple readers at the same time
        :return: None
        """
        self.db_sync.write_to_db(self.key, self.value)

        def read() -> None:
            """
            Read from db and test result
            :return: None
            """
            res = self.db_sync.read_from_db(self.key)

            self.assertEqual(res, self.value)
            LOGGER.debug('finished reading - multiple readers')

        threads = [threading.Thread(target=read) for i in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def test_final(self) -> None:
        """
        Test in different db!
        Final Test
        :return: None
        """
        tmp_db = DbSynchronizer('tmp_db_threads')

        def read(key: Any, result: Any) -> None:
            """
            Read from db and test result.
            :param key: the key to read from the db.
            :param result: the expected result.
            :return: None
            """
            res = tmp_db.read_from_db(key)

            self.assertEqual(res, result)
            LOGGER.debug('finished reading - final test')

        def write(key: Any, value: Any) -> None:
            """
            Write to db and test result
            :param key: the key to write to  the db.
            :param value: the value to write.
            :return: None
            """
            res = tmp_db.write_to_db(key, value)

            self.assertTrue(res)
            LOGGER.debug('finished writing - final test')

        threads = [threading.Thread(target=read, args=["num", None]) for i in range(3)]
        writing_thread = threading.Thread(target=write, args=["num", "12"])
        threads2 = [threading.Thread(target=read, args=["num", "12"]) for i in range(3)]

        for t in threads:
            t.start()

        time.sleep(.001)
        writing_thread.start()
        time.sleep(.001)

        for t in threads2:
            t.start()

        for t in threads + threads2 + [writing_thread]:
            t.join()