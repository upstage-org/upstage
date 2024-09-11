import logging
import pytest
from sqlalchemy import create_engine
from starlette.testclient import TestClient
from bootstraps import app
from config.database import DBSession, engine
from sqlalchemy.orm import sessionmaker
from config.env import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    url=DATABASE_URL,
    echo=True,
    future=True,
)

@pytest.fixture(autouse=True, scope='session')
def db_engine():
    Base.metadata.create_all(engine)
    yield engine 
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def anyio_backend():
  return 'asyncio'

@pytest.fixture(scope='session', autouse=True)
def client():
  with TestClient(app=app, base_url='http://test') as client:
    logging.error('Client is ready')
    yield client



@pytest.fixture(autouse=True, scope='session')
def db_session(db_engine):

    yield DBSession

    DBSession.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        DBSession.execute(f'TRUNCATE {table.name} CASCADE;')
        DBSession.commit()

    DBSession.close()