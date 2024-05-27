"""
This module defines the Flask forms used for admin account creation.
Created by Emmanouel.

The module includes:
- Validators:
    - validate_name: Ensures that names do not contain forbidden characters.
    - validate_password: Ensures that passwords meet the required complexity criteria.

- Form:
    - AdminSignUpForm: Flask form for admin account creation with fields for email, first name, last name,
password, phone, confirm password, date of birth, and address.
"""

import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import Email, ValidationError, DataRequired, Length, EqualTo


def validate_name(form, name):
    """
    Validator to check for forbidden characters in names.
    Created by Emmanouel.

    Args:
        form (FlaskForm): The form instance containing the name field.
        name (Field): The field to validate.

    Raises:
        ValidationError: If the name contains forbidden characters.
    """
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in name.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


def validate_password(form, password):
    """
    Validator to check the password format.
    Created by Emmanouel.

    Args:
        form (FlaskForm): The form instance containing the password field.
        password (Field): The field to validate.

    Raises:
        ValidationError: If the password does not meet the required format.
    """
    pattern = re.compile(r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-z0-9])')

    if not pattern.match(password.data):
        raise ValidationError("Password must contain at least 1 digit, 1 lowercase, 1 uppercase word character and "
                              "1 special character.")


#
class AdminSignUpForm(FlaskForm):
    """
    Signup Form for creating a new admin account.
    Created by Emmanouel.

    This form includes fields for email, first name, last name, password, phone, confirm password, date of birth, and
    address.
    """
    email = StringField(validators=[Email(), DataRequired(), Length(max=60, message="Email must not surpass 60 "
                                                                                    "characters.")])
    first_name = StringField(validators=[DataRequired(), Length(max=40, message="First name must not surpass 100 "
                                                                                "characters."),
                                         validate_name])
    last_name = StringField(validators=[DataRequired(), Length(max=40, message="Last name must not surpass 100 "
                                                                               "characters."), validate_name])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=100, message="Password must be between 8 "
                                                                                        "and 100 characters long."),
                                         validate_password])
    phone = StringField(validators=[DataRequired(), Length(max=11, message='Phone number must not surpass 11 digits.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal')])
    dob = DateField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired(), Length(max=100, message="Address must not surpass 100 characters."
                                                             )])
    submit = SubmitField()

