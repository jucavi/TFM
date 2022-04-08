import logging
from smtplib import SMTPException
from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
from flask import render_template

logger = logging.getLogger(__name__)

def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            logger.exception("Send email: Something went wrong!")


def send_email(subject, sender, recipients, text_body, cc=None, bcc=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body

    if html_body:
        msg.html = html_body

    Thread(target=_send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.set_reset_password_token()

    send_email(subject='TFT Password Reset',
               sender=('TFT', current_app.config['MAIL_DEFAULT_SENDER']),
               recipients=[user.email],text_body=render_template('mailer/auth/reset_password.txt', token=token, user=user),
               html_body=render_template('mailer/auth/reset_password.html', token=token, user=user))


def send_project_invitation(project, user):
    token = project.collaborator_token(user)

    send_email(subject='Project join invitation',
               sender=('TFT', current_app.config['MAIL_DEFAULT_SENDER']),
               recipients=[user.email],text_body=render_template('mailer/project/project_invitation.txt', token=token, user=user, project=project),
               html_body=render_template('mailer/project/project_invitation.html', token=token, user=user, project=project))