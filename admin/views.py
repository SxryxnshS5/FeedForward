from flask import Blueprint, render_template, flash, redirect, url_for, session
from app import db, app
from models import User, Advert, Message, Collection
from admin.forms import AdminSignUpForm
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
                return render_template('errors/403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@admin_blueprint.route('/adminaccount')
@login_required
@requires_roles('admin')
def admin_account():
    """ View function for viewing the admin account details. """

    # get all collected adverts
    collected_adverts = Advert.query.filter_by(available=False).all()
    # get all available adverts
    current_adverts = Advert.query.filter_by(available=True).all()
    # get all users
    current_users = User.query.filter_by(role='user').all()

    # renders the admin account template
    return render_template('main/adminaccount.html', current_adverts=current_adverts, current_users=current_users,
                           collected_adverts=collected_adverts)


@admin_blueprint.route('/create_admin_account', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_admin_account():
    """ view function which is used to create an admin account"""
    # create signup form object
    form = AdminSignUpForm()
    # if request method is POST or form is valid
    if form.validate_on_submit():
        with app.app_context():
            admin = User.query.filter_by(email=form.email.data).first()
            # if this returns a user, then the admin already exists in database
            # if email already exists redirect user back to signup page with error message so user can try again
            if admin:
                flash('Email address already exists')
                return render_template('main/create_admin_account.html', form=form)

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

            flash('New Admin added successfully.')
            return redirect(url_for('admin.admin_account'))
    # if request method is GET or form not valid re-render admin page
    return render_template('main/create_admin_account.html', form=form)


@admin_blueprint.route('/account_overview/<user>')
@login_required
@requires_roles('admin')
def account_overview(user):
    user = User.query.get(user)
    adverts = Advert.query.filter_by(owner=user.id).all()
    orders = Collection.query.filter_by(buyer=user.id).all()
    return render_template('main/account_overview.html', user=user, adverts=adverts, orders=orders, admin_overview=True)


@admin_blueprint.route('/delete_user/<int:user_id>', methods=["GET", "POST"])
@login_required
@requires_roles('admin')
def delete_user(user_id):
    # get user from database
    active_user = User.query.filter_by(id=user_id).first()
    if not active_user.role == 'off':
        # change user role as offline
        active_user.role = 'off'
        # update role change
        db.session.commit()
        # inform admin and redirect to admin account page
        flash("User successfully deleted.")
        return redirect(url_for('admin.admin_account'))

