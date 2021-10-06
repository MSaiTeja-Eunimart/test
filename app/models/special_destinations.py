from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey


class SpecialDestinations(MySqlBase):

    __tablename__ = 'special_destinations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    special_destination_state = Column(String)
    slug = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    is_archive = Column(Boolean)
    state_code = Column(String)
    state_id = Column(Integer, ForeignKey(
        'states.id'))
    
