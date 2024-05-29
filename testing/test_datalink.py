from datetime import datetime, timedelta
import unittest

from models import User, Advert, Collection, Message
from app import app
import datalink

# test values for each table
test_users = [
    ["testemail1@gmail.com", "password", "John", "Smith", datetime.now(),
     "lorem ipsum", "1", "user"],
    ["testemail2@gmail.com", "password", "Eva", "Smith", datetime.now(),
     "lorem ipsum", "1", "user"],
    ["testemail3@gmail.com", "password", "Alex", "Smith", datetime.now(),
     "lorem ipsum", "1", "user"],
    ["testemail4@gmail.com", "password", "Bob", "Smith", datetime.now(),
     "lorem ipsum", "1", "user"],
]

# ads with this use by will always be in date
tomorrow = datetime.today() + timedelta(days=1)
# ads with this use by will always be out of date
yesterday = datetime.today() - timedelta(days=1)

test_adverts = [
    ["in date", "lorem ipsum", 55.0, 1.6, "lorem ipsum", 1, tomorrow, True],
    ["in date", "lorem ipsum", 56.0, 1.4, "lorem ipsum", 2, tomorrow, True],
    ["out of date", "lorem ipsum", 55.0, 1.6, "lorem ipsum", 1, yesterday, True],
    ["out of date", "lorem ipsum", 56.0, 1.4, "lorem ipsum", 2, yesterday, True],
    ["unavailable", "lorem ipsum", 55.0, 1.6, "lorem ipsum", 2, tomorrow, False],
]

test_messages = [
    [1, 2,
     datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "1"],
    [1, 2,
     datetime.strptime("01/01/2001 01:01:02", "%d/%m/%Y %H:%M:%S"), "2"],
    [1, 2,
     datetime.strptime("01/01/2001 01:01:03", "%d/%m/%Y %H:%M:%S"), "3"],
    [3, 4,
     datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "hello world"],
    [1, 3,
     datetime.strptime("01/01/2001 01:01:01", "%d/%m/%Y %H:%M:%S"), "lorem ipsum"],
]

test_collections = [
    # replace adIDs & userIDs after they're auto generated
    [1, 1, 2, datetime.now()],
]


class TestDatabase(unittest.TestCase):
    """Test suite for datalink.py functions
        Created by Rebecca
    """
    def setUp(self):
        """remove any test rows from the database if they are still there from failed tests
            Runs before all other tests
        """
        with app.app_context():
            # get test user emails
            emails = [user[0] for user in test_users]
            users = User.query.filter(User.email.in_(emails))
            # remove any existing test rows
            for user in users:
                datalink.delete_user(user)

            print("count " + str(len(Advert.query.all())))

    def test_connect(self):
        """test datalink can connect to the database"""
        connection = datalink._connect()
        self.assertIsNotNone(connection)

    def test_create_delete_user(self):
        """test a user object can be added and then removed from the database"""
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
        """test an advert object can be added and then removed from the database"""
        with app.app_context():
            # setup
            user = User(*test_users[0])
            datalink.create_user(user)
            advert = Advert(*test_adverts[0])
            advert.owner = user.id
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
        """test a message object can be added and then removed from the database"""
        with app.app_context():
            # setup
            user1 = User(*test_users[0])
            datalink.create_user(user1)
            user2 = User(*test_users[1])
            datalink.create_user(user2)

            # test creation
            test_message = test_messages[0]
            message = Message(*test_message)
            message.sender = user1.id
            message.receiver = user2.id
            datalink.create_message(message)
            q = Message.query.filter_by(sender=user1.id, receiver=user2.id,
                                        timestamp=test_message[2]).first()
            self.assertIsNotNone(q)

            # test deletion
            datalink.delete_message(message)
            q = Message.query.filter_by(sender=user1.id, receiver=user2.id,
                                        timestamp=test_message[2]).first()
            self.assertIsNone(q)

            datalink.delete_user(user1)
            datalink.delete_user(user2)

    def test_create_delete_collection(self):
        """test a collection object can be added and then removed from the database"""
        with app.app_context():
            # setup
            seller = User(*test_users[0])
            datalink.create_user(seller)
            collector = User(*test_users[1])
            datalink.create_user(collector)

            advert = Advert(*test_adverts[0])
            advert.owner = seller.id
            datalink.create_advert(advert)

            # test creation
            test_collect = test_collections[0]
            test_collect[0] = advert.adID
            collection = Collection(*test_collect)
            collection.seller = seller.id
            collection.buyer = collector.id

            datalink.create_order(collection)
            q = Collection.query.filter_by(advert=advert.adID, buyer=collector.id).first()
            self.assertIsNotNone(q)

            # test deletion
            datalink.delete_order(collection)
            q = Collection.query.filter_by(advert=advert.adID, buyer=collector.id).first()
            self.assertIsNone(q)

            datalink.delete_user(seller)
            datalink.delete_user(collector)

    def test_check_expiry(self):
        """test if out of date ads can be marked as unavailable while leaving in date ones alone"""
        with app.app_context():
            # setup
            user1 = User(*test_users[0])
            datalink.create_user(user1)
            user2 = User(*test_users[1])
            datalink.create_user(user2)
            users = [user1, user2]

            ads = []
            for i in range(5):
                ads.append(Advert(*test_adverts[i]))
                # set owner with AA generated id, index 3 points to which test user to use
                ads[i].owner = users[test_adverts[i][5] - 1].id
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
            users = [user1, user2]

            ads = []
            for i in range(5):
                ads.append(Advert(*test_adverts[i]))
                ads[i].owner = users[test_adverts[i][5] - 1].id
                datalink.create_advert(ads[i])

            assert len(ads) == 5

            # check only the 2 available ads were returned
            availables = datalink.get_available_ads()
            self.assertEquals(len(availables), 2)  # only 2 should be available in first 5 test ads
            self.assertEqual(availables[0].title, "in date")
            self.assertEqual(availables[1].title, "in date")

            # remove test rows
            datalink.delete_user(user1)
            datalink.delete_user(user2)

    def test_get_conversations(self):
        """test if get conversations returns only users who have messages with the user"""
        with app.app_context():
            users = [User(*u) for u in test_users]
            for u in users:
                datalink.create_user(u)
            messages = [Message(*m) for m in test_messages]
            for i in range(len(messages)):
                messages[i].sender = users[test_messages[i][0] - 1].id
                messages[i].receiver = users[test_messages[i][1] - 1].id
                datalink.create_message(messages[i])

            conversations = datalink.get_conversations(users[0].id)
            print(conversations)
            self.assertEqual(len(conversations), 2)
            emails = [c.email for c in conversations]
            self.assertIn("testemail2@gmail.com", emails)
            self.assertIn("testemail3@gmail.com", emails)

            for u in users:
                datalink.delete_user(u)

    def test_get_latest_message(self):
        """test that get_latest_message returns the true most recent message from another user"""
        with app.app_context():
            users = [User(*u) for u in test_users]
            for u in users:
                datalink.create_user(u)
            messages = [Message(*m) for m in test_messages]
            for i in range(len(messages)):
                messages[i].sender = users[test_messages[i][0] - 1].id
                messages[i].receiver = users[test_messages[i][1] - 1].id
                datalink.create_message(messages[i])

            recent = datalink.get_latest_message(users[0].id, users[1].id)
            self.assertIsNotNone(recent)
            self.assertEqual(recent.contents, "3")

            for u in users:
                datalink.delete_user(u)

    def test_get_message_history(self):
        """test if get_message history returns the correct messages and in the correct order"""
        with app.app_context():
            users = [User(*u) for u in test_users]
            for u in users:
                datalink.create_user(u)
            messages = [Message(*m) for m in test_messages]
            for i in range(len(messages)):
                messages[i].sender = users[test_messages[i][0] - 1].id
                messages[i].receiver = users[test_messages[i][1] - 1].id
                datalink.create_message(messages[i])

            history = datalink.get_message_history(users[0].id, users[1].id)
            # check messages collected
            self.assertEqual(len(history), 3)
            # check messages in order - should be "1", "2", "3"
            for i in range(3):
                self.assertEquals(history[i].contents, str(i + 1))

            for u in users:
                datalink.delete_user(u)


if __name__ == '__main__':
    unittest.main()
