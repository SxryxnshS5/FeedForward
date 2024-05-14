import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_address = "FeedForwardUK@gmail.com"
password = "okgx wpwq xvio ncei"


def send_welcome_email(User):
    """Function to send a welcome email when a user registers"""
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
