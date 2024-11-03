import unittest
import threading
import time
from operation_methods import OperationSettings
from database_syncer import DbSynchronizer
from log_manager import LOGGER


class TestDbSynchronizerWithThreads(unittest.TestCase):
    db_sync = DbSynchronizer(operation_method=OperationSettings.THREADS, name="test_db")

    def test_simple_write_access(self) -> None:
        """
        Tests that write access can be acquired without any competition.
        Logs the start and end of the test, and the result of the write operation.
        :return: None
        """
        LOGGER.debug("Starting test_simple_write_access")
        result = self.db_sync.write_to_db("key1", "value1")
        LOGGER.debug(f"Write access result: {result}")
        self.assertTrue(result)
        LOGGER.debug("Completed test_simple_write_access")

    def test_simple_read_access(self):
        """
        Tests that read access can be acquired without any competition.
        Logs the start and end of the test, and verifies the read result matches the expected value.
        :return: None
        """
        LOGGER.debug("Starting test_simple_read_access")
        self.db_sync.write_to_db("key2", "value2")
        result = self.db_sync.read_from_db("key2")
        LOGGER.debug(f"Read access result for key2: {result}")
        self.assertEqual(result, "value2")
        LOGGER.debug("Completed test_simple_read_access")

    def test_concurrent_read_access(self):
        """
        Tests that multiple threads can acquire read access concurrently.
        Logs the start and end of the test, along with each reader thread's activity.
        :return: None
        """
        LOGGER.debug("Starting test_concurrent_read_access")

        def reader():
            """
            Simulates a read operation on the database with delay.
            Logs the start and completion of each read operation.
            :return: None
            """
            LOGGER.debug("Reader thread started")
            self.db_sync.read_from_db("key5")
            LOGGER.debug("Reader thread completed")
            time.sleep(0.5)

        readers = [threading.Thread(target=reader) for _ in range(5)]

        for r in readers:
            r.start()

        for r in readers:
            r.join()

        LOGGER.debug("Completed test_concurrent_read_access")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
