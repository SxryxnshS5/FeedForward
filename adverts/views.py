from flask import Blueprint, render_template
from adverts.forms import AdvertForm

adverts_blueprint = Blueprint('adverts', __name__, template_folder='templates')


@adverts_blueprint.route('/create_advert', methods=['GET', 'POST'])
def create_advert():
    form = AdvertForm()
    if form.validate_on_submit():
        print("2")
        return render_template('main/login.html')
    else:
        return render_template('main/createadvert.html', form=form)
