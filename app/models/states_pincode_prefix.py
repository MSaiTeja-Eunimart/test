
from .db_base import MySqlBase
from sqlalchemy import Column, Integer, ForeignKey


class StatesPincodePrefix(MySqlBase):

    __tablename__ = 'states_pincode_prefix'
    id = Column(Integer, primary_key=True, autoincrement=True)
    state_id = Column(Integer, ForeignKey(
        'states.id'))
    state_prefix = Column(Integer)
    