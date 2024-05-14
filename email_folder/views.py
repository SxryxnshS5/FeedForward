import smtplib

from models import User
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from_address = "FeedForwardUK@gmail.com"
password = "okgx wpwq xvio ncei"


def send_welcome_email(User):
    contents = "Hi " + User.get_first_name()
    contents += "\n Welcome to FeedForward! Thank you for signing up."

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = User.get_email()
    msg["Subject"] = "Welcome to FeedForward"
    body = contents
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, User.get_email(), text)
    s.quit()


new_user = User("alex8lines@gmail.com", "test", "alex", "lines", "08/04/2004", "test", "user")
send_welcome_email(new_user)