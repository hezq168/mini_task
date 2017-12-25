# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import current_app
from flask_mail import Mail,Message
from threading import Thread
from config import Config


mail = Mail()


## 异步发送邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)



def send_email(to, subject, content):
    app = current_app._get_current_object()
    msg = Message(subject=subject,sender=Config.MAIL_SENDER,recipients=[to])
    msg.body = 'hello'
    msg.html = content  #邮件内容
    thread = Thread(target=send_async_email,args=[app,msg])
    thread.start()

    # mail.send(msg)


