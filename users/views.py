from flask_login import login_user, logout_user, current_user, login_required
from users.forms import SignUpForm, LoginForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User
from app import db
from markupsafe import Markup

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # create signup form object
    form = SignUpForm()
    # Check if user is logged out
    if current_user.is_anonymous:
        # if request method is POST or form is valid
        if form.validate_on_submit():
            print("PLEASE")
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
                            address=form.address.data)

            # add the new user to the database
            print(new_user)
            db.session.add(new_user)
            db.session.commit()

            # create session variable
            session['email'] = new_user.email
            # sends user to 2fa page
            return redirect(url_for('main/account.html'))
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
    # set authentication attempts to 0 if there is no authentication attempts yet
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0
    form = LoginForm()
    # check if user is logged in
    if current_user.is_anonymous:
        # if request method is POST or form is valid
        if form.validate_on_submit():
            from models import User
            user = User.query.filter_by(email=form.email.data).first()

            # check user exists, password/pin/postcode are all correct
            if not user or not user.verify_password(form.password.data):
                # Increment authentication attempts
                session['authentication_attempts'] += 1
                # check if max number of authentication attempts has been exceeded
                if session.get('authentication_attempts') >= 3:
                    # time out the user
                    flash(Markup(
                        'Number of incorrect login attempts exceeded. Please click <a href = "/reset" > here </a> to reset.'))
                    return render_template('main/login.html')
                else:
                    flash('Incorrect credentials, {} login attempts remaining'.format(
                        3 - session.get('authentication_attempts')))
                    # Generate security log for failed log in
                    # redirect user to login page
                    return render_template('main/login.html', form=form)

            else:
                # create user
                login_user(user)
                current_user.num_logins += 1
                db.session.commit()
                # reset authentication attempts
                session['authentication_attempts'] = 0
                # generate security log for user log in
                # redirect to correct page depending on role
                if current_user.role == 'user':
                    return redirect(url_for('lottery.lottery'))
                else:
                    return redirect(url_for('admin.admin'))
    else:
        # if user is already logged in
        flash('You are already logged in.')
        return render_template('main/account.html')
    return render_template('main/login.html', form=form)
