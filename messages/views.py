from flask_login import login_user, logout_user, current_user, login_required

import datalink
from messages.forms import MessageForm
import bcrypt
from flask import Blueprint, flash, render_template, session, redirect, url_for
from models import User, Advert
from app import db, app
from markupsafe import Markup
from datetime import datetime

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/messages', methods=['GET', 'POST'])
def view_messages():
    # get users messaging current user
    users = datalink.get_conversations(current_user.id)
    # get most recent messages to or from each user
    recent_messages = {u: datalink.get_latest_message(current_user.id, u.id)
                       for u in users}
    time_messages = dict()
    if recent_messages:
        # sort so most recent messages at top
        recent_messages = dict(sorted(recent_messages.items(),
                                      key=lambda x: x[1].timestamp, reverse=True))

        for u in users:
            message = recent_messages[u]
            time_diff = datetime.now() - message.timestamp
            # get how long ago message sent in mins
            time_diff = time_diff.total_seconds() // 60
            # find appropriate message in mins, hours or days
            time_msg = ""
            if time_diff < 1:
                time_msg = "sent just now"
            elif time_diff > 60:  # > 1 hour
                time_diff //= 60
                if time_diff > 24:  # > 1 day
                    time_diff //= 24
                    time_msg = "%d day(s) ago" % time_diff
                else:
                    time_msg = "%d hours(s) ago" % time_diff
            else:
                time_msg = "%d min(s) ago" % time_diff

            time_messages.update({u: time_msg})
    return render_template('main/messages.html',
                           recent_messages=recent_messages, time_messages=time_messages)



@messages_blueprint.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('main/chat.html')
