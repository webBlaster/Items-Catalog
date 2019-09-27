import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return{
            'name': self.name,
            'email': self.email,
            'id': self.id,
            'picture': self.picture,
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category = Column(String(10))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return{
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category': self.category,
            'user_id': self.user_id,
        }


# engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
engine = create_engine('sqlite:///restaurantmenu')
Base.metadata.create_all(engine)
