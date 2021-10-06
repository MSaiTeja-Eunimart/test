from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, Float


class Pincodes(MySqlBase):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String)
    percentage = Column(Float)
