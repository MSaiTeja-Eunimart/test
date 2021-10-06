from .db_base import MySqlBase
from app import db
from sqlalchemy import Column, String, Integer, ForeignKey, Float


class Rates(MySqlBase):

    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)
    weight = Column(Float)
    price = Column(Float)
    cod = Column(Integer)
    cod_percentage = Column(Float)
    special_offers_percentage = Column(Float)
    expected_delivery_time = Column(String)