from flask import Blueprint, render_template
from adverts.forms import AdvertForm
from flask_login import current_user, login_required
from app import db, app
from models import User, Advert

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

            return render_template('main/advert_details.html', current_advert=new_advert)
    else:
        return render_template('main/createadvert.html', form=form)



# View for user account information
@adverts_blueprint.route('/advert_details')
@login_required
def advert_details():
    """
    View function for displaying user account information.
    Requires the user to be logged in.

    Returns:
        flask.Response: Renders the account.html template with user details.
    """
    # Fetch and render user details
    return render_template('main/advert_details.html')