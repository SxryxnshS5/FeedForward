import datalink
import unittest
import datetime
from models import User, Advert, Collection, Message
from app import app, db

class TestDatabase(unittest.TestCase):
    def test_connect(self):
        """test datalink can connect to the database"""
        connection = datalink._connect()
        self.assertIsNotNone(connection)


    def test_create_delete_user(self):
        with app.app_context():

            test_email = "testemail05127i@gmail.com"
            user = User(test_email, "password", "John", "Smith", datetime.datetime.now(), "lorem ipsum", "user")
            datalink.create_user(user)
            # test creation
            q = User.query.filter_by(email=test_email).first()
            self.assertIsNotNone(q)
            # test deletion
            datalink.delete_user(user)
            q = User.query.filter_by(email=test_email).first()
            self.assertIsNone(q)




if __name__ == '__main__':
    unittest.main()