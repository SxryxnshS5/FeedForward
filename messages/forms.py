from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MessageForm(FlaskForm):
    """ Message form for a user to send a message"""

    contents = StringField()
    submit = SubmitField()
