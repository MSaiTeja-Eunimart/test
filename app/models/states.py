from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class States(MySqlBase):

    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    slug = Column(String)
    code = Column(String)
