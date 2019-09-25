from peewee import *

from models.base_model import baseModel
from models.user import User
from models.reply import Reply


class Topic(baseModel):
    views = IntegerField(null=False, default=0)
    title = TextField(null=False)
    content = TextField(null=False)
    user_id = IntegerField(null=False)
    board_id = IntegerField(null=False)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count
