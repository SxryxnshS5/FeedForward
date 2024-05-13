# table = user | advert | foodorder | message

def _connect():
    # connect to food sharing database (only for internal use here)
    pass


def _create(table, **columns):
    # generic private method for creating a row in any table
    pass


def _retrieve(table, columns, condition=None, orderby=None, asc=True,
              limit=None):
    # generic private method for a select query
    pass


def _update(table, new_val, condition=None):
    # generic private method for updating a row in any table
    pass


def _delete(table, condition):
    # generic private method for deleting a row in a table
    pass


def create_user(user):
    """Add a new user row to user table using a User object"""
    pass


def create_advert(advert):
    """Add a new advert row to advert table using an Advert object"""
    pass


def create_order(advert, collector, timestamp):
    """Add new order row to foodorder table
        & mark advert as unavailable
    requires an Advert object & User object
    """
    pass


def create_message(message):
    """Add a new message row to message table using an message object"""
    pass


def get_available_ads():
    """returns list of adverts that are currently available to collect"""
    pass


def get_user(username):
    """returns a User object from the database using their username"""
    pass


def is_unique(username):
    """returns if a username is already in use"""


def set_advert_unavailable(adID):
    """marks advert as unavailable using its ID"""
    pass


def check_expirery():
    """finds and marks all adverts past their expiry date as unavailable"""
    pass


def update_details(old_user, updated_user):
    """updates old_user's details to have updated_user's attribtutes
        - note a new username must be unique
        - note role cannot be changed to admin here
    """


def delete_user(user):
    """removes user object's row in User table"""
    pass


def delete_advert(advert):
    """removes advert object's row in Advert table"""
    pass


def delete_message(message):
    """removes message object's row in Message table"""
    pass



