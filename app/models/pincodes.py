from .db_base import MySqlBase
from sqlalchemy import Column, Integer, ForeignKey, String


class Pincodes(MySqlBase):
    __tablename__ = 'pincodes'
    pincode = Column(Integer, primary_key=True)
    state_name = Column(String)
    city_name = Column(String)