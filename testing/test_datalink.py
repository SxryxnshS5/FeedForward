import datalink
import unittest
import datetime
from models import User, Advert, Collection, Message
from app import app, db

test_users = [
    ["testemail1@gmail.com", "password", "John", "Smith", datetime.datetime.now(), "lorem ipsum", "user"],
    ["testemail2@gmail.com", "password", "Eva", "Smith", datetime.datetime.now(), "lorem ipsum", "user"],
]

test_adverts = [
    ["Title", "lorem ipsum", "lorem ipsum", "testemail1@gmail.com", datetime.datetime.now(), True],
]

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """remove any test rows from the database if they are still there"""
        with app.app_context():
            adIDs = [advert[0] for advert in test_adverts]
            emails = [user[0] for user in test_users]

            ads = Advert.query.filter(Advert.adID.in_(adIDs))
            users = User.query.filter(User.email.in_(emails))

            for ad in ads:
                datalink.delete_advert(ad)

            for user in users:
                datalink.delete_user(user)

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



if __name__ == '__main__':
    unittest.main()