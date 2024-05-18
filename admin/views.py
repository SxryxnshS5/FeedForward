from flask import Blueprint, render_template, flash, redirect, url_for, session
from app import db, app
from models import User, Advert, Message
from admin.forms import AdminSignUpForm
from flask_login import current_user, login_required
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

