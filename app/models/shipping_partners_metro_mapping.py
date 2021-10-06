from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Pincodes(MySqlBase):
    __tablename__ = 'shipping_partner_metro_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shipping_partner_service_mapping_id = Column(Integer, ForeignKey(
        'shipping_partner_service_mapping.id'), primary_key=True)
    metro_city_id = Column(Integer, ForeignKey('metros.id'), primary_key=True)
