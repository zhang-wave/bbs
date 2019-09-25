import hashlib

from peewee import *
import config
import secret
from models.base_model import baseModel

from peewee import *


class User(baseModel):
    default_signature = "“这家伙很懒，什么个性签名都没有留下。”"

    username = CharField(50, null=False, unique=True)
    password = CharField(100, null=False)
    image = CharField(100, null=False, default='/static/images/headers/1.jpg')
    email = CharField(50, null=False, default=config.test_mail)
    signature = CharField(50, null=False, default=default_signature)

    @staticmethod
    def salted_password(password, salt='$!@><?>SKT&RNGa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
