"""python file that contains all the models for the project"""

class User():
    """User class. This is a class for all User objects, and contains
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
    """Advert class. This is a class for all Advert objects, and contains
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
