import datalink
import unittest
from datetime import datetime
from models import User, Advert, Collection, Message
from app import app, db
from sqlalchemy import tuple_

test_users = [
    ["testemail1@gmail.com", "password", "John", "Smith", datetime.now(), "lorem ipsum", "user"],
    ["testemail2@gmail.com", "password", "Eva", "Smith", datetime.now(), "lorem ipsum", "user"],
]

test_adverts = [
    ["Title", "lorem ipsum", "lorem ipsum", "testemail1@gmail.com", datetime.now(), True],
]

test_messages = [
    ["testemail1@gmail.com", "testemail2@gmail.com",
     datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "hello world"]
]

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """remove any test rows from the database if they are still there from failed tests"""
        with app.app_context():
            # get primary keys for each test row
            adIDs = [advert[0] for advert in test_adverts]
            emails = [user[0] for user in test_users]
            messageIDs = [(msg[0], msg[1], msg[2]) for msg in test_messages]

            # find any existing test rows
            ads = Advert.query.filter(Advert.adID.in_(adIDs))
            users = User.query.filter(User.email.in_(emails))
            messages = Message.query.filter(
                tuple_(Message.sender, Message.receiver, Message.timestamp).in_(messageIDs))

            # remove any existing test rows
            for ad in ads:
                datalink.delete_advert(ad)

            for user in users:
                datalink.delete_user(user)

            for msg in messages:
                datalink.delete_user(msg)

    def test_connect(self):
        """test datalink can connect to the database"""
        connection = datalink._connect()
        self.assertIsNotNone(connection)

    def test_create_delete_user(self):
        with app.app_context():
            test_email = test_users[0][0]
            user = User(*test_users[0])
            datalink.create_user(user)
            # test creation
            q = User.query.filter_by(email=test_email).first()
            self.assertIsNotNone(q)
            # test deletion
            datalink.delete_user(user)
            q = User.query.filter_by(email=test_email).first()
            self.assertIsNone(q)

    def test_create_delete_advert(self):
        with app.app_context():
            # setup
            user = User(*test_users[0])
            datalink.create_user(user)
            advert = Advert(*test_adverts[0])
            datalink.create_advert(advert)
            id = advert.adID

            # test creation
            q = Advert.query.filter_by(adID=id).first()
            self.assertIsNotNone(q)
            # test deletion
            datalink.delete_advert(advert)
            datalink.delete_user(user)
            q = User.query.filter_by(email=id).first()
            self.assertIsNone(q)

    def test_create_delete_message(self):
        with app.app_context():
            # setup
            user1 = User(*test_users[0])
            datalink.create_user(user1)
            user2 = User(*test_users[1])
            datalink.create_user(user2)

            # test creation
            test_message = test_messages[0]
            message = Message(*test_message)
            datalink.create_message(message)
            q = Message.query.filter_by(sender=test_message[0], receiver=test_message[1],
                                        timestamp=test_message[2]).first()
            self.assertIsNotNone(q)

            # test deletion
            datalink.delete_message(message)
            datalink.delete_user(user1)
            datalink.delete_user(user2)
            q = Message.query.filter_by(sender=test_message[0], receiver=test_message[1],
                                        timestamp=test_message[2]).first()
            self.assertIsNone(q)


if __name__ == '__main__':
    unittest.main()