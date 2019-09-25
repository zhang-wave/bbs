from sqlalchemy import create_engine

from peewee import *
import secret
from app import configured_app
from flask_sqlalchemy import SQLAlchemy
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User

import pymysql


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    conn = SQLAlchemy()
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS webflask')
        c.execute('CREATE DATABASE webflask CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE webflask')

    conn.metadata.create_all(bind=e)

    d = {'host': 'localhost', 'password': '{}'.format(secret.database_password),
         'port': 3306, 'user': 'root'}
    db = MySQLDatabase('webflask', **d)
    with db:
        db.drop_tables([Board, Reply, Topic, User])
        db.create_tables([Board, Reply, Topic, User])


def generate_fake_date():
    form = dict(
        username='test',
        password='123',
    )
    u = User.register(form)

    form = dict(
        username='zed',
        password='123',
    )
    u = User.register(form)

    form = dict(
        username='zzzz',
        password='123',
    )
    u = User.register(form)

    form = dict(
        title='all'
    )
    b = Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )

    for i in range(10):
        print('begin topic <{}>'.format(i))
        t = Topic.new(topic_form, u.id)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
        )
        for j in range(5):
            Reply.new(reply_form, u.id)


if __name__ == '__main__':
    reset_database()
    generate_fake_date()
