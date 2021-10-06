
from .db_base import MySqlBase
from sqlalchemy import Column, Integer, ForeignKey


class ExtraChargesServiceMapping(MySqlBase):

    __tablename__ = 'extra_charges_service_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey(
        'shipping_partner_service_mapping.id'), primary_key=True)
    gst = Column(Integer)
    fuel_charges = Column(Integer)
    eunimart_charges = Column(Integer)
    extra_surcharges = Column(Integer)
