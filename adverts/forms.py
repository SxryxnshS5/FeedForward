from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField
from wtforms.validators import Email, ValidationError, DataRequired, Length, EqualTo


class AdvertForm(FlaskForm):
    """ Advert Form with the required fields for a user to create an advert"""

    title = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    contents = StringField(validators=[DataRequired()])
    expiry = DateField(validators=[DataRequired()])
    submit = SubmitField()
