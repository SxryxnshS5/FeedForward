import re
from flask_wtf import FlaskForm, Recaptcha
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField
from wtforms.validators import Email, ValidationError, DataRequired, Length, EqualTo


# Validator to check forbidden characters in names
def validate_name(form, name):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in name.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


# Validator to check password format
def validate_password(form, password):

    pattern = re.compile(r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-z0-9])')

    if not pattern.match(password.data):
        raise ValidationError("Password must contain at least 1 digit, "
                              "1 lowercase, 1 uppercase word character and "
                              "1 special character.")


# Signup Form
class SignupForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    name = StringField(validators=[DataRequired(), validate_name])
    password = PasswordField(validators=[DataRequired, Length(min=8), validate_password])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal')])
    birthday = DateField(validators=[DataRequired])
    address = StringField(validators=[DataRequired])
    submit = SubmitField()


# Login Form
class Login(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    postcode = StringField(validators=[DataRequired()])
    #recaptcha = RecaptchaField()
    submit = SubmitField()
