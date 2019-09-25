from peewee import *
from models.base_model import baseModel
from models.user import User


class Reply(baseModel):

    content = TextField(null=False)
    topic_id = IntegerField(null=False)
    user_id = IntegerField(null=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m


