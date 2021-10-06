from .db_base import MySqlBase
from sqlalchemy import Column, Integer, ForeignKey, Boolean


class AreaServed(MySqlBase):
    __tablename__ = 'areas_served'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pincodes_id = Column(Integer, ForeignKey(
        'pincodes.pincode'), primary_key=True)
    shipping_partner_service_mapping_id = Column(Integer, ForeignKey(
        'shipping_partner_service_mapping.id'), primary_key=True)
    pickup = Column(Boolean)
    delivery = Column(Boolean)
    cod = Column(Boolean)
    prepaid = Column(Boolean)
    return_shipment = Column(Boolean)