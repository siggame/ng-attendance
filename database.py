from sqlalchemy import create_engine
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
import json


engine = create_engine('sqlite:///db.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class DeveloperInfo(Base):
    __tablename__ = 'developerInfo'

    id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    preferred_name = Column(String)
    email = Column(String, primary_key=True)
    github_username = Column(String)
    team = Column(String)
    planning_to_compete = Column(Boolean)
    added_manually = Column(Boolean, default=True)
    attendances = relationship("Attendance")

    def __repr__(self):
        fmt = "<Developer(name='{} {}', github_username='{}')>"
        return fmt.format(self.first_name, self.last_name, self.github_username)

    def to_dict(self):
        fields = {c.name: c.type.python_type(getattr(self, c.name))
                  for c in self.__table__.columns}

        attendance = Attendance.latest_for(self)
        fields['here'] = attendance.here if attendance else False
        return fields

    def to_json(self):
        return json.dumps(self.to_dict())

    def update(self, items):
        for column, value in items.iteritems():
            if column not in ('id', ):
                setattr(self, column, value)
        return self

    @staticmethod
    def from_dict(items):
        d = DeveloperInfo()
        d.update(items)
        d.id = DeveloperInfo.next_id()
        db_session.add(d)
        db_session.commit()
        return d

    @staticmethod
    def all():
        return db_session.query(DeveloperInfo).all()

    @staticmethod
    def get(id):
        return db_session.query(DeveloperInfo).filter(DeveloperInfo.id==id).first()

    @staticmethod
    def next_id():
        max = db_session.query(DeveloperInfo.id).order_by(DeveloperInfo.id.desc()).first()
        if max is None:
            return 0
        return max.id + 1


class Attendance(Base):

    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    dev = Column(Integer, ForeignKey('developerInfo.id'))
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    here = Column(Boolean)

    def to_dict(self):
        return {'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'here': self.here,
                'dev': self.dev}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def latest_for(dev):
        if len(dev.attendances) > 0:
            return dev.attendances[-1]

        a = Attendance(dev=dev.id, here=False)
        db_session.add(a)
        db_session.commit()
        return a

    @staticmethod
    def mark(dev, here=True):
        latest = Attendance(dev=dev.id, here=here)
        db_session.add(latest)
        db_session.commit()
        return latest


def init_db():
    Base.metadata.create_all(bind=engine)
