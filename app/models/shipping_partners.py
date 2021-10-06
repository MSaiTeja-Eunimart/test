from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer


class ShippingPartners(MySqlBase):

    __tablename__ = 'shipping_partners'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    slug = Column(String)
