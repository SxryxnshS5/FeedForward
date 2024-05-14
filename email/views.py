from models import User

def send_welcome_email(User):
    contents = "Hi " + User.get_name()
