
from .db_base import MySqlBase
from sqlalchemy import Column, Integer, ForeignKey


class MetrosPincodePrefix(MySqlBase):

    __tablename__ = 'metros_pincode_prefix'
    id = Column(Integer, primary_key=True, autoincrement=True)
    metro_city_id = Column(Integer, ForeignKey(
        'metros.id'))
    metro_prefix_code = Column(Integer)
    