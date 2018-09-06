from flask import current_app, render_template

from app import mail
from flask_mail import Message
#
def send_email(to, subject, template, **kwargs):
    msg = Message('[ZTY]' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template,**kwargs)

    mail.send(msg)

