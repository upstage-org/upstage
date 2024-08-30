from sqlalchemy import create_engine, MetaData
from databases import Database
from .env import DATABASE_URL
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

db = declarative_base()

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

def get_scoped_session():
    session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    session.begin()
    return session