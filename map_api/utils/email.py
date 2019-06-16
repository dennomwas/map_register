from flask_mail import Message

from map_api import mail


def send_mail(
        subject, sender, recipients, template, body=None):
    msg = Message(
        subject,
        sender=sender,
        recipients=recipients,
        html=template,
        body=body
    )
    mail.send(msg)
