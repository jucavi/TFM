from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.message.forms import MessageForm
from app.message.models import Message
from app.auth.models import User
from app import db


msg_bp = Blueprint('message',
                    __name__,
                    static_folder='static',
                    template_folder='templates')


@msg_bp.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    # users = User.query.all()
    form = MessageForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(email=form.email.data).first()
        if recipient:
            message = Message(sender_id=current_user.id, recipient_id=recipient.id, body=form.message.data)

            db.session.add(message)
            db.session.commit()
            flash('Your message has been sent.', category='success')
            return redirect(url_for('project.all'))
        else:
            flash('')
    return render_template('send_message.html',
                           title='Send message',
                           form=form)


@msg_bp.route('/all')
@login_required
def all():
    messages = Message.query.all()
    return 'All messages'