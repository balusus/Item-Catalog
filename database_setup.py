import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Component(Base):
    __tablename__ = 'component'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    image = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'image': self.image,
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))

    component_id = Column(Integer, ForeignKey('component.id'))
    component = relationship(Component)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }


engine = create_engine('postgresql+psycopg2://grader:udacity@localhost/catalog')
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
