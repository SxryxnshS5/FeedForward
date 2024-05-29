from flask_login import login_user, logout_user, current_user, login_required

import datalink
from messages.forms import MessageForm

from flask import Blueprint, flash, render_template, jsonify, session
from models import User, Message
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
                    time_msg = "sent %d day(s) ago" % time_diff
                else:
                    time_msg = "sent %d hours(s) ago" % time_diff
            else:
                time_msg = "sent %d min(s) ago" % time_diff

            time_messages.update({u: time_msg})
    return render_template('messages/messages.html',
                           recent_messages=recent_messages, time_messages=time_messages, current_page='view_messages')


@messages_blueprint.route('/<int:id>/chat', methods=['GET', 'POST'])
def chat(id):
    # store messanger id to be used for updating messages later with JS
    session['messager'] = id
    form = MessageForm()
    # send new message if POST
    if form.validate_on_submit():
        new_msg = Message(current_user.id, id, datetime.now(), form.contents.data)
        datalink.create_message(new_msg)

    # show conversation
    messages = datalink.get_message_history(current_user.id, id)
    user = datalink.get_user_from_id(id)
    name = user.first_name
    return render_template('messages/chat.html', form=form, conversation=messages, name=name, current_page='view_messages')

@messages_blueprint.route('/update_chat', methods=['POST'])
def update_chat():
    id = session['messager']
    messages = datalink.get_message_history(current_user.id, id)
    return jsonify({'messages': render_template('messages.html', conversation=messages)})
