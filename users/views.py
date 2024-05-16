from flask_login import login_user, logout_user, current_user, login_required
from users.forms import SignUpForm, LoginForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # create signup form object
    form = SignUpForm()
    # Check if user is logged out
    if current_user.is_anonymous:
        print(1)
        # if request method is POST or form is valid
        if form.validate_on_submit():
            print(2)
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
    print("YBDHCBHJBVBHSDFBHJSDBHJU")
    return render_template('main/signup.html', form=form)


