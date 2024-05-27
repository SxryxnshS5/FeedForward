from flask_login import login_user, logout_user, current_user, login_required

import users.views
from users.forms import SignUpForm, LoginForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User, Advert, Collection
from app import db, app
from email_folder.views import send_welcome_email
from markupsafe import Markup

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """Function that provides the functionality of the signup form.
    Created by Alex, amended by Suryansh and Rebecca

    Returns:
        flask.Response: Returns either the login.html template if the sign up is successful, the account.html
        template if the user is logged in, or the signup.html template if unsuccessful
    """
    # create signup form object
    form = SignUpForm()
    # Check if user is logged out
    if current_user.is_anonymous:
        # if request method is POST or form is valid
        if form.validate_on_submit():
            with app.app_context():
                user = User.query.filter_by(email=form.email.data).first()
                # if this returns a user, then the email already exists in database
                # if email already exists redirect user back to signup page with error message so user can try again
                if user:
                    flash('Email address already exists')
                    return render_template('main/signup.html', form=form)

                # create a new user with the form data
                new_user = User(email=form.email.data,
                                first_name=form.first_name.data,
                                surname=form.last_name.data,
                                password=bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()),
                                role='user',
                                dob=form.dob.data,
                                address=form.address.data,
                                phone=form.phone.data)

                # add the new user to the database

                db.session.add(new_user)
                db.session.commit()

                # create session variable
                session['email'] = new_user.email
                send_welcome_email(new_user)
                return redirect(url_for('users.login'))

    else:
        # if user is already logged in
        flash('You are already logged in.')
        # send user to account page
        return render_template('main/account.html')
    # if request method is GET or form not valid re-render signup page
    return render_template('main/signup.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Function that provides the functionality of the login form.
    Created by Alex, amended by Suryansh and Emmanouel

    Returns:
        flask.Response: Renders either the login.html template or the account.html template with the correct
        user details
    """
    # set authentication attempts to 0 if there is no authentication attempts yet
    form = LoginForm()
    print("1")
    # check if user is logged in
    if current_user.is_anonymous:
        print("2")
        # if request method is POST or form is valid
        if form.validate_on_submit():
            print("3")
            with app.app_context():
                from models import User
                user = User.query.filter_by(email=form.email.data).first()
                print("4")

                # check user exists, password/pin/postcode are all correct
                if not user or not user.verify_password(form.password.data):
                    flash('Incorrect details')
                    return render_template('main/login.html', form=form)
                # check if user account is still active
                if user.role == 'off':
                    flash('This account no longer exists')
                    return render_template('main/login.html', form=form)

                else:
                    # create user
                    login_user(user)
                    db.session.commit()

                    # redirect to correct page depending on role
                    if current_user.role == 'user':
                        return redirect(url_for('users.account'))
                    else:
                        return redirect(url_for('admin.admin_account'))
    else:
        # if user is already logged in
        adverts = Advert.query.filter_by(owner=current_user.id).all()
        flash('You are already logged in.')
        return render_template('main/account.html', adverts=adverts)
    return render_template('main/login.html', form=form)


# View for user account information
@users_blueprint.route('/account')
@login_required
def account():
    """
    View function for displaying user account information.
    Requires the user to be logged in.
    Created by Suryansh, amended by Alex

    Returns:
        flask.Response: Renders the account.html template with user details.
    """
    # Fetch user details and adverts
    user_details = {
        'email': current_user.email,
        'first_name': current_user.first_name,
        'surname': current_user.surname,
        'dob': current_user.dob,
        'address': current_user.address,
        'phone': current_user.phone,
        'role': current_user.role
    }

    adverts = Advert.query.filter_by(owner=current_user.id, available=True).all()
    orders = Collection.query.filter_by(buyer=current_user.id).all()

    return render_template('main/account.html', current_user=user_details, adverts=adverts, orders=orders)


@users_blueprint.route('/logout')
@login_required
def logout():
    """Function to log the user out"""
    # Log the user out
    logout_user()
    # Clear the session
    session.clear()
    # Redirect to the login page or home page
    flash('You have been logged out.')
    return redirect(url_for('users.login'))
