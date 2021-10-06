
from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class Cities(MySqlBase):

    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    slug = Column(String)
