"""python file that contains all the models for the project"""

class User():
    """User class that acts as a template for all User objects, and contains
    all of a user's attributes and methods, as well as the constructor
    for a User object"""

    def __init__(self, email, password, name, dob, address, role):
        """Constructor for User class"""
        self.email = email
        self.password = password
        self.name = name
        self.dob = dob
        self.address = address
        self.role = role
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

    def set_name(self, new_name):
        """Setter for name variable"""
        self.name = new_name

    def get_name(self):
        """Getter for name variable"""
        return self.name

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


class Advert():
    """Advert class that acts as a template for all Advert objects, and contains
    all of an Advert's attributes and methods, as well as the constructor
    for an Advert object"""

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
   

class Collection():
    """Collection class that acts as a template for all collection objects.
    When an order is reserved, a collection object is made that
    contains all the details of the transaction"""

    def __init__(self,advert, seller, buyer, date):
        """Constructor for Collection class"""
        self.advert = advert
        self.seller = seller
        self.buyer = buyer
        self.date = date
        