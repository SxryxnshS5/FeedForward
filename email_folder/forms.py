from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import Email, ValidationError, DataRequired, Length, EqualTo


class NewsletterForm(FlaskForm):

    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()
