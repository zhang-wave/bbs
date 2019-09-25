from time import sleep

from marrow.mailer import Mailer
from peewee import *
from config import admin_mail
import secret
from models.base_model import baseModel
from models.user import User
from tasks import send_async_simple, send_async


def configured_mailer():
    config = {
        # 'manager.use': 'futures',
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


mailer = configured_mailer()


def send_mail(subject, author, to, content):
    # 延迟测试
    # sleep(30)
    m = mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content

    mailer.send(m)


class Messages(baseModel):
    title = TextField(null=False)
    content = TextField(null=False)
    sender_id = IntegerField(null=False)
    receiver_id = IntegerField(null=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Messages.new(form)

        receiver: User = User.one(id=receiver_id)
        # by default
        # send_mail(
        #     subject=title,
        #     author=admin_mail,
        #     to=receiver.email,
        #     content='站内信通知：\n {}'.format(content),
        # )
        # by thread
        # import threading
        # form = dict(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content'],
        # )
        # t = threading.Thread(target=send_mail, kwargs=form)
        # t.start()

        # by celery
        send_async.delay(
            subject=form['title'],
            author=admin_mail,
            to=receiver.email,
            plain=form['content']
        )
