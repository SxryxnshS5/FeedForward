import datalink
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from users.forms import SignUpForm, LoginForm
from models import User
from flask_login import login_user, logout_user, login_required, current_user


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """ view function which is used to sign a user up in the database"""
    # check if the user is not logged in (anonymous)
    if current_user.is_anonymous:

        # create a SignUp form object
        form = SignUpForm()

        if form.validate_on_submit():
            # check if the user already exists in the db
            user = User.query.filter_by(email=form.email.data).first()

            # if user already exists, inform user so they can try to sign up again.
            if user:
                flash("User already exists.")
                return render_template('main/signup.html')

            # if there is not a user with the same details, create a new user object
            new_user = User(first_name=form.first_name.data,
                            surname=form.last_name,
                            email=form.email.data,
                            dob=form.dob.data,
                            address=form.address.data,
                            password=form.password.data,
                            role='user')

            # add the new user to the db
            datalink.create_user(new_user)

            # redirect user to login page
            return redirect(url_for('main.login'))
    else:
        # if user is logged in (not anonymous) and is trying to log in again, redirect them to main page
        flash('You are already logged in.')
        return render_template('main/index.html')

    return render_template('main/signup.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ view function to log a user in """
    # create a LoginForm object
    form = LoginForm()

    if form.validate_on_submit():
        # find user in the db with their email (if they don't exist it will be null)
        user = User.query.filter_by(email=form.email.data).first()

        # check if the user exists in the database and the password given is correct
        if not user or not user.verify_password(form.password.data):
            # if user does not exist or the password is wrong, inform the user
            flash('Please check your login details and try again.')
            return render_template('main/login.html', form=form)
        else:
            # if the credentials are correct, log the user in and redirect them to the main page
            login_user(user)

            if user.role == 'user':
                # if the user has a user role, redirect them to the main page
                return redirect(url_for('main.index'))
            else:
                # if the user is an admin, redirect them to the admin page
                return redirect(url_for('main.admin'))

    return render_template('main/login.html', form=form)
