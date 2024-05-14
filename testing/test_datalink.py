import datalink
import unittest

class TestDatabase(unittest.TestCase):
    def test_connect(self):
        """test datalink can connect to the database"""
        connection = datalink._connect()
        self.assertIsNotNone(connection)


if __name__ == '__main__':
    unittest.main()