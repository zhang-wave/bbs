from datetime import datetime
from peewee import *
from playhouse.db_url import connect
from string import Template
import secret

d = {'host': 'localhost', 'password': '{}'.format(secret.database_password),
                                         'port': 3306, 'user': 'root'}
# db = MySQLDatabase('webflask', **d)
db = connect(Template('mysql://$user:$password@$host:$port/webflask').substitute(**d))


class baseModel(Model):
    # id = AutoField(default=1)
    create_time = DateTimeField(default=datetime.now, verbose_name='创建时间')
    update_time = DateTimeField(default=datetime.now, verbose_name='更新时间')

    class Meta:
        database = db

    @classmethod
    def new(cls, form):
        m = cls.create(**form)
        return m

    @classmethod
    def update(cls, id, **kwargs):
        # u.username = 'test'
        # db.session.add(u)
        # db.session.commit()
        kwargs['update_time'] = datetime.now()
        cls.update(**kwargs).where(id=id).execute()

    def delete(self):
        self.delete_instance()

    @classmethod
    def all(cls, **kwargs):
        sql_where = ''
        # (User.is_editor == True) |
        # (User.is_admin == True)
        if len(kwargs) > 0:
            sql_where = ' AND '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )
            sql_where = 'WHERE {}'.format(sql_where)
        sql = 'SELECT * FROM {} {}'.format(str(cls.__name__), sql_where)
        ms = []
        # ms = cls.select().where(SQL(sql_where, tuple(kwargs.values())))
        q = cls.raw(sql, *tuple(kwargs.values()))
        for obj in q:
            ms.append(obj)
        return ms

    @classmethod
    def one(cls, **kwargs):
        try:
            ms = cls.get(**kwargs)
            return ms
        except Exception:
            return None

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d


class SimpleUser(baseModel):
    username = CharField(50, null=False, unique=True)
    password = CharField(100, null=False)


if __name__ == '__main__':
    db.create_tables([SimpleUser, ])
    form = dict(
        username='123',
        password='456',
    )
    u = SimpleUser.new(form)
    # print(u)
    u = SimpleUser.one(username='123')
    # print(u)

