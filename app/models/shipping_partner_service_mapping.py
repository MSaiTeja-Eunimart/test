from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


class ShippingPartnerServiceMapping(MySqlBase):

    __tablename__ = 'shipping_partner_service_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('services.id'))
    aggregator_id = Column(Integer, ForeignKey('aggregators.id'))
    shipping_partner_id = Column(Integer, ForeignKey('shipping_partners.id'))
    is_part_of_aggregator = Column(Integer) 
    shipping_partner_service_name = Column(String)
    aggregator_shipping_partner_id = Column(String)
    transit_time = Column(String)
    cut_off_time = Column(String)
