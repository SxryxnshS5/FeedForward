import datalink
import unittest
from datetime import datetime, timedelta
from models import User, Advert, Collection, Message
from app import app, db
from sqlalchemy import or_

# test values for each table
test_users = [
    ["testemail1@gmail.com", "password", "John", "Smith", datetime.now(), "lorem ipsum", "1", "user"],
    ["testemail2@gmail.com", "password", "Eva", "Smith", datetime.now(), "lorem ipsum", "1", "user"],
    ["testemail3@gmail.com", "password", "Alex", "Smith", datetime.now(), "lorem ipsum", "1", "user"],
    ["testemail4@gmail.com", "password", "Bob", "Smith", datetime.now(), "lorem ipsum", "1", "user"],
]

# ads with this use by will always be in date
tomorrow = datetime.today() + timedelta(days=1)
# ads with this use by will always be out of date
yesterday = datetime.today() - timedelta(days=1)

test_adverts = [
    ["in date", "lorem ipsum", "lorem ipsum", "testemail1@gmail.com", tomorrow, True],
    ["in date", "lorem ipsum", "lorem ipsum", "testemail2@gmail.com", tomorrow, True],
    ["out of date", "lorem ipsum", "lorem ipsum", "testemail1@gmail.com", yesterday, True],
    ["out of date", "lorem ipsum", "lorem ipsum", "testemail2@gmail.com", yesterday, True],
    ["unavailable", "lorem ipsum", "lorem ipsum", "testemail2@gmail.com", tomorrow, False],
]

test_messages = [
    ["testemail1@gmail.com", "testemail2@gmail.com",
     datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "1"],
    ["testemail2@gmail.com", "testemail1@gmail.com",
         datetime.strptime("01/01/2001 01:01:02", "%d/%m/%Y %H:%M:%S"), "2"],
    ["testemail1@gmail.com", "testemail2@gmail.com",
         datetime.strptime("01/01/2001 01:01:03", "%d/%m/%Y %H:%M:%S"), "3"],
    ["testemail3@gmail.com", "testemail4@gmail.com",
         datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "hello world"],
]

test_collections = [
    # replace adIDs after they're auto generated
    [1, "testemail1@gmail.com", "testemail2@gmail.com", datetime.now()],
]

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """remove any test rows from the database if they are still there from failed tests"""
        with app.app_context():
            # get test user emails
            emails = [user[0] for user in test_users]
            users = User.query.filter(User.email.in_(emails))
            # remove any existing test rows
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
            q = Advert.query.filter_by(adID=id).first()
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

    def test_create_delete_collection(self):
        with app.app_context():
            # setup
            seller = User(*test_users[0])
            datalink.create_user(seller)
            collector = User(*test_users[1])
            datalink.create_user(collector)

            advert = Advert(*test_adverts[0])
            datalink.create_advert(advert)

            # test creation
            test_collect = test_collections[0]
            test_collect[0] = advert.adID
            collection = Collection(*test_collect)

            datalink.create_order(collection)
            q = Collection.query.filter_by(advert=test_collect[0], buyer=test_collect[2]).first()
            self.assertIsNotNone(q)

            # test deletion
            datalink.delete_order(collection)
            datalink.delete_user(seller)
            datalink.delete_user(collector)
            q = Collection.query.filter_by(advert=test_collect[0], buyer=test_collect[2]).first()
            self.assertIsNone(q)

    def test_check_expiry(self):
        """test if out of date ads can be marked as unavailable while leaving in date ones alone"""
        with app.app_context():
            # setup
            user1 = User(*test_users[0])
            datalink.create_user(user1)
            user2 = User(*test_users[1])
            datalink.create_user(user2)

            ads = []
            for i in range(5):
                ads.append(Advert(*test_adverts[i]))
                datalink.create_advert(ads[i])

            # check in date ads not set to unavailable
            assert len(ads) == 5
            datalink.check_expiry()
            availables = Advert.query.filter_by(title="in date").all()
            for ad in availables:
                self.assertEqual(ad.available, True)

            # check out of date ads set to unavailable
            unavailables = Advert.query.filter_by(title="out of date").all()
            for ad in unavailables:
                self.assertEqual(ad.available, False)


            # remove test rows
            datalink.delete_user(user1)
            datalink.delete_user(user2)

    def test_get_available_with_outdateds(self):
        """test selecting available adverts and removing ones that are out of date"""
        with app.app_context():
            # setup
            user1 = User(*test_users[0])
            datalink.create_user(user1)
            user2 = User(*test_users[1])
            datalink.create_user(user2)

            ads = []
            for i in range(5):
                ads.append(Advert(*test_adverts[i]))
                datalink.create_advert(ads[i])

            assert len(ads) == 5

            # check only the 2 available ads were returned
            availables = datalink.get_available_ads()
            self.assertEquals(len(availables), 2) # only 2 should be available in first 5 test ads
            self.assertEqual(availables[0].title, "in date")
            self.assertEqual(availables[1].title, "in date")

            # remove test rows
            datalink.delete_user(user1)
            datalink.delete_user(user2)

    def test_get_message_history(self):
        with app.app_context():
            users = [User(*u) for u in test_users]
            for u in users:
                datalink.create_user(u)
            messages = [Message(*m) for m in test_messages]
            for m in messages:
                datalink.create_message(m)

            history = datalink.get_message_history("testemail1@gmail.com", "testemail2@gmail.com")
            # check messages collected
            self.assertEqual(len(history), 3)
            # check messages in order - should be "1", "2", "3"
            for i in range(3):
                self.assertEquals(history[i].contents, str(i+1))

            for u in users:
                datalink.delete_user(u)

if __name__ == '__main__':
    unittest.main()