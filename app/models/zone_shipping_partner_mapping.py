from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, ForeignKey


class ZoneShippingPartnerMapping(MySqlBase):
    __tablename__ = 'zone_shipping_partner_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id = Column(Integer, ForeignKey('zones.zone_id'), primary_key=True)
    shipping_partner_id = Column(Integer, ForeignKey(
        'shipping_partners.id'), primary_key=True)
    shipping_partner_zone = Column(String)
    lower_limit = Column(Integer)
    upper_limit = Column(Integer)
