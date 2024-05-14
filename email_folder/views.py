from models import User


from_address = "FeedForwardUK@gmail.com"
def send_welcome_email(User):
    contents = "Hi " + User.get_first_name()
    contents += "\n Welcome to FeedForward!"