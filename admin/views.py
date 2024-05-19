from flask import Blueprint, render_template, flash, redirect, url_for, session
from app import db, app
from models import User, Advert, Message
from admin.forms import AdminSignUpForm, AdminChangeDetailsForm
from flask_login import current_user, login_required, logout_user
from functools import wraps
import bcrypt

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# custom decorator for role based access
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # if role of current user is not one of the authorised ones, redirect them to main page
            if current_user.role not in roles:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@admin_blueprint.route('/create_admin_account', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_admin_account():
    """ view function which is used to create an admin account"""
    # create signup form object
    form = AdminSignUpForm()
    # Check if admin is logged out
    if current_user.is_anonymous:
        # if request method is POST or form is valid
        if form.validate_on_submit():
            with app.app_context():
                admin = User.query.filter_by(email=form.email.data).first()
                # if this returns a user, then the admin already exists in database
                # if email already exists redirect user back to signup page with error message so user can try again
                if admin:
                    flash('Email address already exists')
                    return render_template('main/adminaccount.html', form=form)

                # create a new admin with the form data
                new_admin = User(email=form.email.data,
                                 first_name=form.first_name.data,
                                 surname=form.last_name.data,
                                 password=bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()),
                                 role='admin',
                                 dob=form.dob.data,
                                 address=form.address.data,
                                 phone=form.phone.data)

                # add the new user to the database

                db.session.add(new_admin)
                db.session.commit()

                # create session variable
                session['email'] = new_admin.email
                return render_template('main/adminaccount.html', current_user=new_admin)
    else:
        # if admin is already logged in
        flash('You are already logged in.')
        # send admin to account page
        return render_template('main/adminaccount.html')
    # if request method is GET or form not valid re-render admin page
    return render_template('main/adminaccount.html', form=form)


#CHECK IF BLUEPRINT ROUTE IS CORRECT WITH HTML
@admin_blueprint.route('/current_adverts')
@login_required
@requires_roles('admin')
def current_adverts():
    """ function to view all current adverts """
    with app.app_context():
        # get all adverts in the database which are available
        current_adverts = Advert.query.filter_by(available=True).all()
    return render_template('main/adminaccount.html', current_adverts=current_adverts)


#CHECK IF BLUEPRINT ROUTE IS CORRECT WITH HTML
@admin_blueprint.route('/users')
@login_required
@requires_roles('admin')
def view_users():
    """ function to view all the users of the system """
    with app.app_context():
        # get all the users in the database
        current_users = User.query.filter_by(role='user').all()
    return render_template('main/adminaccount.html', current_users=current_users)


@admin_blueprint.route('/logout')
@login_required
@requires_roles('admin')
def logout():
    """ function to log the admin out """
    # log the admin out
    logout_user()
    # clear the session
    session.clear()
    # inform admin and redirect them to the main page
    flash('You have been logged out.')
    return redirect(url_for('users.index'))


@admin_blueprint.route('/change_details')
@login_required
@requires_roles('admin')
def change_details():
    """ view function which is used to change the details of an admin account """
    form = AdminChangeDetailsForm()
    # check admin is logged in
    if not current_user.anonymous:
        if form.validate_on_submit():
            with app.app_context():
                # check new password is not the same as the current one
                if current_user.verify_password(form.password.data):
                    flash('The new password must not match the current one.')
                    # SHOULD RENDER A CHANGE DETAILS HTML???
                    return render_template('main/adminaccount.html', form=form)
                else:
                    # update all the user details
                    current_user.email = form.email.data
                    current_user.first_name = form.first_name.data
                    current_user.last_name = form.last_name.data
                    current_user.dob = form.dob.data
                    current_user.address = form.address.data
                    current_user.phone = form.phone.data
                    current_user.password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())

                    # commit updates to database
                    db.session.commit()

                    # inform admin about updated details
                    flash ('Admin account details changes successfully.')
                    return render_template('main/adminaccount.html')
    # if request method is GET or form not valid re-render admin page
    # RENDER CHANGE DETAILS PAGE ??
    return render_template('main/change_details.html', form=form)

