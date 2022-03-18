from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.message.forms import MessageForm
from app.message.models import Message
from app.auth.models import User
from app import db
import json


message = Blueprint('message',
                    __name__,
                    static_folder='static',
                    template_folder='templates')


@message.route('/send', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    emails = {'elements': [user.email for user in User.query.all() if user != current_user]}

    if form.validate_on_submit():
        send = False
        author = current_user
        subject = form.subject.data
        body = form.body.data
        mail_list = form.recipients.data

        for email in mail_list:
            recipient = User.query.filter_by(email=email).first()
            if recipient:
                message = Message(author=author,
                                  recipient=recipient,
                                  subject=subject,
                                  body=body)
                db.session.add(message)
                send = True
            else:
                flash(f'User {email!r} not found.', category='warning')

        if send:
            db.session.commit()
            flash('Your message(s) has been sent.', category='success')
        return redirect(url_for('projects.all_projects'))


    return render_template('send_message.html',
                           title='Send message',
                           form=form,
                           hidden_elements=json.dumps(emails))


@message.route('/')
@login_required
def all_messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()

    messages = current_user.messages_received.order_by(Message.timestamp.desc())
    return render_template('_inbox_messages.html', messages=messages)


@message.route('/message/<uuid:message_id>')
@login_required
def show_message(message_id):
    message = Message.query.get(message_id)
    if message in current_user.messages_received:
        print('im in')
        message.read = True
        db.session.add(message)
        db.session.commit()

        return render_template('show_message.html',
                           message=message,
                           title='Message')

    flash('No message found.')
    return redirect(request.referrer)


@message.route('/__inbox_messages')
def __inbox_messages():
    return {'inbox_messages_count': current_user.inbox_messages}