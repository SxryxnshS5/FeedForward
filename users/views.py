from flask_login import login_user, logout_user, current_user, login_required
from users.forms import RegisterForm, LoginForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()
    # Check if user is logged out
    if current_user.is_anonymous:
        # if request method is POST or form is valid
        if form.validate_on_submit():
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
            db.session.add(new_user)
            db.session.commit()


            # create session variable
            session['email'] = new_user.email
            # sends user to 2fa page
            return redirect(url_for('users.setup_2fa'))
    else:
        # if user is already logged in
        flash('You are already logged in.')
        # send user to account page
        return render_template('main/account.html')
    # if request method is GET or form not valid re-render signup page
    return render_template('main/signup.html', form=form)

