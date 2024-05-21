from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    """ Message form for a user to send a message"""

    contents = StringField(validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField()
