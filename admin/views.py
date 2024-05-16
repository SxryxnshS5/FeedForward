from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from models import User, Advert, Message
from admin.forms import AdminSignUpForm
from flask_login import current_user, login_required
from functools import wraps
import datalink

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
    form = AdminSignUpForm()
    """ view function which is used to create an admin account"""
    # create a SignUp form object
    form = AdminSignUpForm

    if form.validate_on_submit():
        # check if the user already exists in the db
        admin = User.query.filter_by(email=form.email.data).first()

        # if admin already exists, inform user and re-render the admin page.
        if admin:
            flash("Admin already exists.")
            return render_template('main/adminaccount.html')

        # if there is not a admin with the same details, create a new user object
        new_admin = User(first_name=form.first_name.data,
                         surname=form.last_name,
                         email=form.email.data,
                         dob=form.birthday.data,
                         address=form.address.data,
                         password=form.password.data,
                         role='admin')

        # add the new admin to the db
        datalink.create_user(new_admin)

        # redirect admin to main admin page
        return redirect(url_for('main.adminaccount'))
    return render_template('main/adminaccount.html', form=form)