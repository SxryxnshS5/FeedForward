import logging
import datalink
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from users.forms import SignUpForm, LoginForm
from models import User
from flask_login import login_user, logout_user, login_required, current_user


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """ view function which is used to sign a user up in the database"""
    # create a SignUp form object
    form = SignUpForm


    if form.validate_on_submit():
        # check if the user already exists in the db
        user = datalink.get_user(form.email.data)

        # if user already exists, inform user so they can try to sign up again.
        if user:
            flash("User already exists.")
            return render_template('main/signup.html')

        # if there is not a user with the same details, create a new user object
        new_user = User(first_name=form.first_name.data,
                        surname=form.last_name,
                        email=form.email.data,
                        dob=form.birthday.data,
                        address=form.address.data,
                        password=form.password.data,
                        role='user')

        # add the new user to the db
        datalink.create_user(new_user)

        # redirect user to login page
        return redirect(url_for('main.login'))

    return render_template('main/signup.html', form=form)


@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    """view function to log a user in"""
    # create a LoginForm object
    form = LoginForm()

    if form.validate_on_submit():

    return render_template('main/login.html', form=form)

