import sys
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80),nullable = False)
    id = Column(Integer,primary_key = True)
    description = Column(String(250))
    category = Column(String(10))

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return{
            'name':self.name,
            'description':self.description,
            'id':self.id,
            'category':self.category,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)