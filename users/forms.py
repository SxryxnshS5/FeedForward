""" python file containing flask forms for user related actions"""

import re
from flask_wtf import FlaskForm, Recaptcha
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField
from wtforms.validators import Email, ValidationError, DataRequired, Length, EqualTo


def validate_name(form, name):
    """ Validator to check forbidden characters in names """

    excluded_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in name.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


def validate_password(form, password):
    """ Validator to check password format """

    pattern = re.compile(r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-z0-9])')

    if not pattern.match(password.data):
        raise ValidationError("Password must contain at least 1 digit, "
                              "1 lowercase, 1 uppercase word character and "
                              "1 special character.")


#
class SignUpForm(FlaskForm):
    """ Signup Form containing all the details needed for a user to create an account"""

    email = StringField(validators=[Email(), DataRequired()])
    first_name = StringField(validators=[DataRequired(), validate_name])
    last_name = StringField(validators=[DataRequired(), validate_name])
    password = PasswordField(validators=[DataRequired(), Length(min=8), validate_password])
    phone = StringField(validators=[DataRequired(), Length(max=11, message='Phone number is too long. Should be 11 '
                                                                           'digits max.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal')])
    dob = DateField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    """ Login Form containing the required fields for a user to log in"""

    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
