from flask_login import login_user, logout_user, current_user, login_required
from users.forms import SignUpForm, LoginForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User, Advert
from app import db, app
from markupsafe import Markup

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """Function that provides the functionality of the signup form"""
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
                # sends user to 2fa page
                return render_template('main/account.html', current_user=new_user)
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
    """Function that provides the functionality of the login form"""
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

                else:
                    # create user
                    login_user(user)
                    db.session.commit()
                    # generate security log for user log in

                    adverts = Advert.query.filter_by(owner=current_user.id).all()

                    # redirect to correct page depending on role
                    if current_user.role == 'user':
                        return render_template('main/account.html', adverts=adverts)
                    else:
                        return render_template('main/adminaccount.html')
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
    
    adverts = Advert.query.filter_by(owner=current_user.id).all()

    return render_template('main/account.html', current_user=user_details, adverts=adverts)
