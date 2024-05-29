"""
This python file defines the routes and view functions for the admin section of the application.
Created by Emmanouel.

The file includes the following functionalities:
- Role-based access control using custom decorators.
- Viewing admin account details, including collected adverts, current adverts, and current users.
- Creating new admin accounts.
- Viewing a detailed account overview for individual users, including their adverts and order history.
- Deleting users by changing their role to 'off'.

Routes:
- /adminaccount: View admin account details.
- /create_admin_account: Create a new admin account.
- /account_overview/<user>: View account overview for a specific user.
- /delete_user/<int:user_id>: Delete a user by changing their role to 'off'.

Functions:
- requires_roles(*roles): Custom decorator for role-based access control.
- admin_account(): View function for viewing admin account details.
- create_admin_account(): View function to create a new admin account.
- account_overview(user): View function to display account overview for a specific user.
- delete_user(user_id): View function to delete a user.

"""

from flask import Blueprint, render_template, flash, redirect, url_for
from app import db, app
from models import User, Advert, Collection
from admin.forms import AdminSignUpForm
from flask_login import current_user, login_required
from functools import wraps
import bcrypt

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


def requires_roles(*roles):
    """
    Custom decorator for role-based access control.
    Created by Emmanouel, amended by Suryansh.

    Args:
        *roles: The roles that are authorized to access the decorated route.

    Returns:
        function: The wrapped function if the current user's role is authorized, otherwise renders a 403 error page.
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # if role of current user is not one of the authorised ones, redirect them the equivalent error pages
            if current_user.role not in roles:
                return render_template('errors/403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@admin_blueprint.route('/adminaccount')
@login_required
@requires_roles('admin')
def admin_account():
    """
    View function for viewing the admin account details.
    Requires the user to be logged in.
    Requires 'admin' role to be authorized.
    Created by Emmanouel.

    Returns:
        flask.Response: Renders the admin account template with collected adverts, current adverts, current users,
        current admins and deleted adverts.
    """
    # get all available adverts
    current_adverts = Advert.query.filter_by(available=True).all()
    # get all users
    current_users = User.query.filter_by(role='user').all()
    # get all admins
    current_admins = User.query.filter_by(role='admin').all()

    # get all unavailable adverts
    unavailable_adverts = Advert.query.filter_by(available=False).all()
    # get all collected advert IDs
    collected_advert_ids = [collection.advert for collection in Collection.query.all()]
    # find the deleted adverts (unavailable adverts not in collected adverts)
    deleted_adverts = [advert for advert in unavailable_adverts if advert.adID not in collected_advert_ids]
    # find the collected adverts (unavailable adverts in collected adverts)
    collected_adverts = [advert for advert in unavailable_adverts if advert.adID in collected_advert_ids]

    # renders the admin account template
    return render_template('admin/admin_account.html', current_adverts=current_adverts, current_users=current_users,
                           current_admins=current_admins, collected_adverts=collected_adverts,
                           deleted_adverts=deleted_adverts, current_page='admin_account')


@admin_blueprint.route('/create_admin_account', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_admin_account():
    """
    View function to create an admin account.
    Requires the user to be logged in.
    Requires 'admin' role to be authorized.
    Created by Emmanouel.

    Returns: flask.Response: Renders the create admin account template. If the form is submitted and valid,
    creates a new admin and redirects to the admin account page.
    """
    # create signup form object
    form = AdminSignUpForm()
    # if request method is POST or form is valid
    if form.validate_on_submit():
        with app.app_context():
            admin = User.query.filter_by(email=form.email.data).first()
            # if this returns a user, then the admin already exists in database
            # if email already exists redirect user back to admin creation page with error message so user can try again
            if admin:
                flash('Email address already exists')
                return render_template('admin/create_admin_account.html', form=form)

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

            flash('New Admin added successfully')
            return redirect(url_for('admin.admin_account'))
    # if request method is GET or form not valid re-render admin page
    return render_template('admin/create_admin_account.html', form=form)


@admin_blueprint.route('/account_overview/<user>')
@login_required
@requires_roles('admin')
def account_overview(user):
    """
    View function to display the account overview for a specific user.
    Requires the user to be logged in.
    Requires 'admin' role to be authorized.
    Created by Emmanouel.

    Args:
        user (str): The ID of the user.

    Returns:
        flask.Response: Renders the account overview template with user details, adverts, and orders.
    """
    # get user from database
    user = User.query.get(user)
    # get all adverts created by specific user
    adverts = Advert.query.filter_by(owner=user.id).all()
    # get all orders collected from specific user
    orders = Collection.query.filter_by(buyer=user.id).all()
    return render_template('admin/account_overview.html', user=user, adverts=adverts, orders=orders, admin_overview=True)


@admin_blueprint.route('/delete_user/<int:user_id>', methods=["GET", "POST"])
@login_required
@requires_roles('admin')
def delete_user(user_id):
    """
    View function to delete a user by changing their role to 'off'.
    Requires the user to be logged in.
    Requires 'admin' role to be authorized.
    Created by Emmanouel.

    Args:
        user_id (int): The ID of the user to be deleted.

    Returns:
        flask.Response: Redirects to the admin account page with a success message.
    """
    # get user from database
    active_user = User.query.filter_by(id=user_id).first()
    if not active_user.role == 'off':
        # change user role as offline
        active_user.role = 'off'
        # update role change
        db.session.commit()
        # inform admin and redirect to admin account page
        flash("User successfully deleted")
        return redirect(url_for('admin.admin_account'))

