
from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, DateTime, Boolean


class Metros(MySqlBase):

    __tablename__ = 'metros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    metro_city = Column(String)
    slug = Column(String)
    create_date = Column(DateTime)
    updated_date = Column(DateTime)
    is_archive = Column(Boolean)
