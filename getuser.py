
# IMPORTS FOR CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, User, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

def check():
    session = DBSession()
    query = session.query(User).all()
    for user in query:
        print user.name
        print user.id

check()