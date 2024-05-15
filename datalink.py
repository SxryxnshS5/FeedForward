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



def get_user(email):
    """returns a User object from the database using their username"""
    return User.query.filter_by(email=email).first()


def is_unique(email):
    """returns if a username isn't already in use"""
    return get_user(email) is None

def set_advert_unavailable(adID):
    """marks advert as unavailable using its ID"""
    ad = Advert.query.filter_by(adID=adID).first()
    ad.available = False
    db.session.commit()


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
    if updated_user.role == "admin" and old_user.role != "admin":
        raise ValueError("Cannot change role to admin")
    if not is_unique(updated_user.email):
        raise ValueError("Username unavailable")

    old_user.email = updated_user.email
    old_user.password = updated_user.password
    old_user.first_name = updated_user.first_name
    old_user.surname = updated_user.surname
    old_user.dob = updated_user.dob
    old_user.address = updated_user.address
    old_user.role = updated_user.role
    db.session.commit()


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



