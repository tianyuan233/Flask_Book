from app import mail
from flask_mail import Message
#to, subject, template, **kwargs
def send_email():
    msg = Message('测试',sender='1406282384@qq.com',body='Tets',
                  recipients=['17691076523@163.com'])
    mail.send(msg)

