import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from app import db, app
from models import User, Advert, Message, Collection
from datetime import datetime

def _connect():
    # connect to database, only use internally for testing
    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:password@localhost:3306/2033foodsharing")
    try:
        engine.connect()
        print("connected")
        return engine
    except SQLAlchemyError as e:
        print("error", e.__cause__)
        return None

def create_user(user):
    """Add a new user row to user table using a User object"""
    db.session.add(user)
    db.session.commit()


def create_advert(advert):
    """Add a new advert row to advert table using an Advert object"""
    db.session.add(advert)
    db.session.commit()


def create_order(order):
    """Add new order row to foodorder table"""
    db.session.add(order)
    db.session.commit()


def create_message(message):
    """Add a new message row to message table using an message object"""
    db.session.add(message)
    db.session.commit()


def get_available_ads():
    """returns list of adverts that are currently available to collect
        autimatically marks out of date ads as unavailable
    """
    check_expiry()
    return Advert.query.filter_by(available=True).all()



def get_user(username):
    """returns a User object from the database using their username"""
    pass


def is_unique(username):
    """returns if a username is already in use"""


def set_advert_unavailable(adID):
    """marks advert as unavailable using its ID"""
    pass


def check_expiry():
    """finds and marks all adverts past their expiry date as unavailable"""
    # equivalent to UPDATE Advert SET available=False WHERE available AND expiry < now
    Advert.query.filter(
        and_(Advert.available, Advert.expiry < datetime.now())
    ).update({Advert.available: False})
    db.session.commit()


def update_details(old_user, updated_user):
    """updates old_user's details to have updated_user's attribtutes
        - note a new username must be unique
        - note role cannot be changed to admin here
    """


def delete_user(user):
    """removes user object's row in User table"""
    db.session.delete(user)
    db.session.commit()


def delete_advert(advert):
    """removes advert object's row in Advert table"""
    db.session.delete(advert)
    db.session.commit()


def delete_message(message):
    """removes message object's row in Message table"""
    db.session.delete(message)
    db.session.commit()


def delete_order(order):
    """removes order object's row in foodorder table"""
    db.session.delete(order)
    db.session.commit()



