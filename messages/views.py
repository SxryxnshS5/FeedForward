from datetime import datetime

from flask import Blueprint, render_template, jsonify, session
from flask_login import current_user, login_required

import datalink
from messages.forms import MessageForm
from models import Message


messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/messages', methods=['GET', 'POST'])
@login_required
def view_messages():
    """Function that provides the functionality of the messages page form.
        Allows user to view all users they have a conversation with and their most recent message
        Clicking on any of these conversations will redirect to the appropriate chat page
        Requires user to be logged in
        Created by Rebecca

        Returns:
            flask.Response: returns the messages.html template with appropriate conversation
            data passed
        """
    # get users messaging current user
    users = datalink.get_conversations(current_user.id)
    # get most recent messages to or from each user
    recent_messages = {u: datalink.get_latest_message(current_user.id, u.id)
                       for u in users}
    time_messages = {}
    if recent_messages:
        # sort so most recent messages at top
        recent_messages = dict(sorted(recent_messages.items(),
                                      key=lambda x: x[1].timestamp, reverse=True))

        for u in users:
            # find how long ago most recent message was sent
            message = recent_messages[u]
            time_diff = datetime.now() - message.timestamp
            # get how long ago message sent in mins
            time_diff = time_diff.total_seconds() // 60
            # find appropriate message in mins, hours or days and add to dict
            time_msg = ""
            if time_diff < 1:
                time_msg = "sent just now"
            elif time_diff > 60:  # > 1 hour
                time_diff //= 60
                if time_diff > 24:  # > 1 day
                    time_diff //= 24
                    time_msg = f"sent {time_diff} day(s) ago"
                else:
                    time_msg = f"sent {time_diff} hours(s) ago"
            else:
                time_msg = f"sent {time_diff} min(s) ago"

            time_messages.update({u: time_msg})
    return render_template('messages/messages.html',
                           recent_messages=recent_messages, time_messages=time_messages,
                           current_page='view_messages')


@messages_blueprint.route('/<int:id>/chat', methods=['GET', 'POST'])
@login_required
def chat(messanger_id):
    """Function that provides the functionality of the chat page form.
            Allows user to view all messages they have with another user with id 'messanger_id' and
                send a new one
            Requires user to be logged in
            Created by Rebecca

            Returns:
                flask.Response: returns the chat.html template with appropriate message data passed
            """
    # store messanger id to be used for updating messages later with JS
    session['messager'] = messanger_id
    form = MessageForm()
    # send new message if POST
    if form.validate_on_submit():
        new_msg = Message(current_user.id, messanger_id, datetime.now(), form.contents.data)
        datalink.create_message(new_msg)

    # show conversation
    messages = datalink.get_message_history(current_user.id, messanger_id)
    user = datalink.get_user_from_id(messanger_id)
    name = user.first_name
    return render_template('main/chat.html', form=form, conversation=messages, name=name)

@messages_blueprint.route('/update_chat', methods=['POST'])
@login_required
def update_chat():
    """Function that provides server side functionality to live updating messages with JS ajax
            uses session data to find the 2 communicating users and new messages between them

            NOTE: Not currently in use

            Returns:
                flask.Response: json storing replacement html for list of messages in chat.html
                                with key 'messages'
            """
    messanger_id = session['messager']
    messages = datalink.get_message_history(current_user.id, messanger_id)
    return jsonify({'messages': render_template('update_message.html', conversation=messages)})
