from flask_login import login_user, logout_user, current_user, login_required
from messages.forms import MessageForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User, Advert
from app import db, app
from markupsafe import Markup

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/messages', methods=['GET', 'POST'])
def send_messages():
    form = MessageForm

    return render_template()
