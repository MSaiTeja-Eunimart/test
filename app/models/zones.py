from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class Zones(MySqlBase):

    __tablename__ = 'zones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    slug = Column(String)
    zone_name = Column(String)
