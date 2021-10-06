
from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import ActiveRecordMixin, SerializeMixin, SmartQueryMixin
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class MySqlBase(Base, ActiveRecordMixin, SerializeMixin, SmartQueryMixin, db.Model):
    __abstract__ = True
    
    def __repr__(self):
        # name = self.name if hasattr(self, "name") else self.id
        if hasattr(self, "name"):
            name = self.name
        elif hasattr(self, "pincode"):
            name = self.pincode
        else:
            name = self.id

        return "{}('{}')".format(self.__class__.__name__, name)


MySqlBase.set_session(db.session)