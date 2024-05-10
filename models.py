"""python file that contains all the models for the project"""

class User():
    """User class. This class is an object for all users, and contains
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
