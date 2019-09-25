import time

from sqlalchemy import Unicode, Column
from peewee import *
from models.base_model import baseModel


class Board(baseModel):
    # title = Column(Unicode(50), nullable=False)
    title = TextField(null=False)
