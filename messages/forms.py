from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MessageForm(FlaskForm):
    """ Login Form containing the required fields for a user to log in"""

    contents = StringField()
    submit = SubmitField()
