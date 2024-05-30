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
from datetime import datetime, timedelta

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


def validate_dob(form, field):
    """
    Validator to ensure the user is at least 18 years old and not older than 100 years old.
    Created by Emmanouel.

    Args:
        form (FlaskForm): The form instance containing the dob field.
        field (Field): The field to validate.

    Raises:
        ValidationError: If the date of birth is not within the valid age range.
    """
    today = datetime.today()
    dob = field.data
    min_age = 18
    max_age = 100
    min_date = today - timedelta(days=min_age * 365)  # Approximate minimum age in days
    max_date = today - timedelta(days=max_age * 365)  # Approximate maximum age in days

    if dob > min_date.date():
        raise ValidationError('You must be at least 18 years old to sign up.')
    if dob < max_date.date():
        raise ValidationError('You must be less than 100 years old to sign up.')


def validate_phone(form, field):
    """
    Validator to ensure the phone number contains only digits.
    Created by Emmanouel.

    Args:
        form (FlaskForm): The form instance containing the phone field.
        field (Field): The field to validate.

    Raises:
        ValidationError: If the phone number contains non-digit characters.
    """
    phone = field.data
    if not phone.isdigit():
        raise ValidationError('Phone number must contain only digits.')


def validate_address(form, field):
    """
    Validator to ensure the address contains only valid characters.
    Created by Emmanouel.

    Args:
        form (FlaskForm): The form instance containing the address field.
        field (Field): The field to validate.

    Raises:
        ValidationError: If the address contains invalid characters.
    """
    address = field.data
    if not re.match(r'^[a-zA-Z0-9\s,.-/\\]*$', address):
        raise ValidationError('Address must contain only letters, numbers, spaces, and common punctuation marks '
                              '(,.-/\\).')


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
    phone = StringField(validators=[DataRequired(), Length(max=11, message='Phone number must not surpass 11 digits.'),
                                    validate_phone])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal')])
    dob = DateField(validators=[DataRequired(), validate_dob])
    address = StringField(validators=[DataRequired(), Length(max=100, message="Address must not surpass 100 characters."
                                                             ), validate_address])
    submit = SubmitField()

