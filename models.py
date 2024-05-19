"""python file that contains all the models for the project"""
from datetime import datetime

from app import db, app
from flask_login import UserMixin
import bcrypt


class User(db.Model, UserMixin):
    """User class that acts as a template for all User objects, and contains
    all of a user's attributes and methods, as well as the constructor
    for a User object"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(5), nullable=False, default='user')
    phone = db.Column(db.String(11), nullable=False)

    adverts = db.relationship('Advert', cascade="all,delete")
    sent_messages = db.relationship('Message', foreign_keys='[Message.sender]',
                                    cascade="all,delete")
    received_messages = db.relationship('Message', foreign_keys='[Message.receiver]',
                                        cascade="all,delete")
    collected_orders = db.relationship('Collection', foreign_keys='[Collection.buyer]',
                                       cascade="all,delete")
    sold_orders = db.relationship('Collection', foreign_keys='[Collection.seller]',
                                  cascade="all,delete")

    def __init__(self, email, password, first_name, surname, dob, address, phone, role):
        """Constructor for User class"""
        self.email = email
        self.password = password
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.address = address
        self.role = role
        self.phone = phone
        self.messages = []

    def set_email(self, new_email):
        """Setter for email variable"""
        self.email = new_email

    def get_email(self):
        """Getter for email variable"""
        return self.email

    def set_password(self, new_password):
        """Setter for password variable"""
        self.password = new_password

    def get_password(self):
        """Getter for password variable"""
        return self.password

    def set_first_name(self, new_name):
        """Setter for first name variable"""
        self.first_name = new_name

    def get_first_name(self):
        """Getter for first name variable"""
        return self.first_name

    def set_surname(self, new_surname):
        """Setter for surname variable"""
        self.surname = new_surname

    def get_surname(self):
        """Getter for surname variable"""
        return self.surname

    def set_dob(self, new_dob):
        """Setter for dob variable"""
        self.dob = new_dob

    def get_dob(self):
        """Getter for dob variable"""
        return self.dob

    def set_address(self, new_address):
        """Setter for address variable"""
        self.address = new_address

    def get_address(self):
        """Getter for address variable"""
        return self.address

    def get_role(self):
        """Getter for role variable"""
        return self.role

    def verify_password(self, plain_password):
        """Function to check submitted password matches with the database password (compared after encrypting the
        submitted password) """
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password = self.password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password)


class Advert(db.Model):
    """Advert class that acts as a template for all Advert objects, and contains
    all of an Advert's attributes and methods, as well as the constructor
    for an Advert object"""

    __tablename__ = 'advert'
    adID = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.ForeignKey(User.id), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, nullable=False)

    def __init__(self, title, address, contents, owner, expiry, available=True):
        """Constructor for Advert class"""
        self.title = title
        self.address = address
        self.contents = contents
        self.owner = owner
        self.expiry = expiry
        self.available = available

    def set_title(self, new_title):
        """Setter for title variable"""
        self.title = new_title

    def get_title(self):
        """Getter for title variable"""
        return self.title

    def set_address(self, new_address):
        """Setter for address variable"""
        self.address = new_address

    def get_address(self):
        """Getter for address variable"""
        return self.address

    def set_contents(self, new_contents):
        """Setter for contents variable"""
        self.contents = new_contents

    def get_contents(self):
        """Getter for contents variable"""
        return self.contents

    def get_owner(self):
        """Getter for owner variable"""
        return self.owner

    def set_expiry(self, new_expiry):
        """Setter for expiry variable"""
        self.expiry = new_expiry

    def get_expiry(self):
        """Getter for expiry variable"""
        return self.expiry

    def set_available(self, new_available):
        """Setter for available variable"""
        self.available = new_available

    def get_available(self):
        """Getter for available variable"""
        return self.available


class Collection(db.Model):
    """Collection class that acts as a template for all Collection objects.
    When an order is reserved, a collection object is made that
    contains all the details of the transaction"""

    __tablename__ = 'foodorder'
    advert = db.Column('adID', db.ForeignKey(Advert.adID), primary_key=True,
                       nullable=False)
    buyer = db.Column('buyerID', db.ForeignKey(User.id), primary_key=True,
                      nullable=False)
    seller = db.Column('sellerID', db.ForeignKey(User.id), nullable=False)
    date = db.Column('timestamp', db.DateTime, nullable=False)

    def __init__(self, advert, seller, buyer, date):
        """Constructor for Collection class"""
        self.advert = advert
        self.seller = seller
        self.buyer = buyer
        self.date = date


class Message(db.Model):
    """Message class that acts as a template for all Message objects.
    When a user sends a message to another user, a message object is
    created and then added to that users Messages list"""

    __tablename__ = 'message'
    sender = db.Column('senderID', db.ForeignKey(User.email), primary_key=True,
                       nullable=False)
    receiver = db.Column('receiverID', db.ForeignKey(User.email), primary_key=True,
                         nullable=False)
    timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)
    contents = db.Column(db.String(200), nullable=False)

    def __init__(self, sender, receiver, timestamp, contents):
        """Constructor for Message class"""
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.contents = contents


class Email():
    """Email class that acts as a template for all Email objects
    When we want to send an email, we create an Email object that
    contains all the data for the email"""

    def __init__(self, users, title, contents):
        """Constructor for email class"""
        self.users = users
        self.title = title
        self.contents = contents


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        new_user = User("a","a","b","c", datetime.strptime("08/01/2004", "%d/%m/%Y"), "a", "1","user")
        db.session.add(new_user)
        db.session.commit()
