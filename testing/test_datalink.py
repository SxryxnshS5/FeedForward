import datalink
import unittest

class TestDatabase(unittest.TestCase):
    def test_connect(self):
        """test datalink can connect to the database"""
        connection = datalink._connect()
        self.assertTrue(connection is not None)
        self.assertTrue(connection.is_connected())