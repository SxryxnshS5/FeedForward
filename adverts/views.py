import datetime
import json

from flask import Blueprint, render_template, redirect, url_for, session, request
from adverts.forms import AdvertForm
from flask_login import current_user, login_required
from app import db, app
from models import User, Advert, Collection
from sqlalchemy.sql import func

adverts_blueprint = Blueprint('adverts', __name__, template_folder='templates')


@adverts_blueprint.route('/create_advert', methods=['GET', 'POST'])
@login_required
def create_advert():
    """Function that provides the functionality of the advert form"""
    form = AdvertForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=current_user.email).first()
            new_advert = Advert(title=form.name.data,
                                address=form.address.data,
                                contents=form.contents.data,
                                expiry=form.expiry.data,
                                owner=user.id)

            db.session.add(new_advert)
            db.session.commit()

            return redirect(url_for('adverts.advert_details', advert=new_advert.adID))
    else:
        return render_template('main/createadvert.html', form=form)


# View for user account information
@adverts_blueprint.route('/advert_details/<advert>')
@login_required
def advert_details(advert):
    """
    View function for displaying advert information.
    Requires the user to be logged in.

    Returns:
        flask.Response: Renders the advert_details.html template with advert details.
    """
    # Fetch and render user details

    return render_template('main/advert_details.html', current_advert=Advert.query.get(advert))


@adverts_blueprint.route('/list_adverts')
@login_required
def list_adverts():
    adverts = Advert.query.filter_by(available=True)
    return render_template('main/listedadverts.html', current_advert=adverts)


@adverts_blueprint.route('/collect_confirmation/<advert>')
@login_required
def collect_confirmation(advert):

    with app.app_context():
        current_advert = Advert.query.get(advert)
        current_advert.available = False
        new_collection = Collection(advert=current_advert.adID,
                                    buyer=current_user.id,
                                    seller=current_advert.owner,
                                    date=datetime.datetime.now())

        db.session.add(new_collection)
        db.session.commit()
        return render_template('main/collect-confirmation.html', current_advert=current_advert)

