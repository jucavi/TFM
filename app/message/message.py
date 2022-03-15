from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.message.forms import MessageForm
from app.message.models import Message
from app.auth.models import User
from app import db


messages = Blueprint('messages',
                    __name__,
                    static_folder='static',
                    template_folder='templates')


@messages.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    # users = User.query.all()
    form = MessageForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(email=form.email.data).first()
        if recipient:
            message = Message(author=current_user, recipient=recipient, body=form.message.data)

            db.session.add(message)
            db.session.commit()
            flash('Your message has been sent.', category='success')
            return redirect(url_for('projects.all_projects'))
        else:
            flash('User not found.', category='warning')
    return render_template('send_message.html',
                           title='Send message',
                           form=form)


@messages.route('/messages')
@login_required
def all_messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()

    messages = current_user.messages_received.order_by(Message.timestamp.desc())
    return render_template('_inbox_messages.html', messages=messages)


@messages.route('/message/<uuid:message_id>')
@login_required
def show_message(message_id):
    message = Message.query.get(message_id)
    if message in current_user.messages_received:
        return render_template('show_message.html',
                           message=message,
                           title='Message')

    flash('No message found.')
    return redirect(request.referrer)