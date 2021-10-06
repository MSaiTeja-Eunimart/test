from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, ForeignKey


class Cities(MySqlBase):

    __tablename__ = 'shipping_partner_sdes_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shipping_partner_service_mapping_id = Column(Integer, ForeignKey(
        'shipping_partner_service_mapping.id'), primary_key=True)
    metro_city_id = Column(Integer, ForeignKey('metros.id'), primary_key=True)
    special_destination_id = Column(Integer, ForeignKey(
        'special_destinations.id'), primary_key=True)
