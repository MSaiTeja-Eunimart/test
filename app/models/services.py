from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class Services(MySqlBase):

    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    services = Column(String)
    slug = Column(String)
