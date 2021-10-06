from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class Aggregators(MySqlBase):

    __tablename__ = 'aggregators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregator_id = Column(String)
    aggregator_name = Column(String)
    slug = Column(String)
