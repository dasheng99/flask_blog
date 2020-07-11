from app.extensions import mail
from flask_mail import Message
from flask import current_app,render_template


def send_mail(to,subject,template,**kwargs):
    msg = Message(subject=subject,
                  recipients=[to],
                  sender=current_app.config['MAIL_USERNAME']
                  )
    msg.html = render_template(template+'.html',**kwargs)
    msg.body = render_template(template+'.txt',**kwargs)
    mail.send(message=msg)
    return '邮件已发送'