import smtplib
from flask import Blueprint, flash, render_template, session, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_folder.forms import NewsletterForm
from models import User
from app import db, app

from_address = "FeedForwardUK@gmail.com"
password = "okgx wpwq xvio ncei"


email_blueprint = Blueprint('email', __name__, template_folder='templates')


def send_welcome_email(User):
    """Function to send a welcome email when a user registers
    Created by Alex"""
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


@email_blueprint.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                user.newsletter = 1
                db.session.commit()
                contents = "Hi " + user.get_first_name()
                contents += "\n Thank you for signing up to our newsletter!"

                msg = MIMEMultipart()
                msg['From'] = from_address
                msg['To'] = user.get_email()
                msg["Subject"] = "FeedForward Newsletter"
                body = contents
                msg.attach(MIMEText(body, 'plain'))

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(from_address, password)
                text = msg.as_string()
                s.sendmail(from_address, user.get_email(), text)
                s.quit()

                flash('You have subscribed to our newsletter')
                return redirect(url_for('email.newsletter'))
            else:
                flash("We couldn't find that email in our database!")

    return render_template('general/newsletter.html', form=form)


