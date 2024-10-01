import logging
import time
import pytest
from sqlalchemy import create_engine, text
from starlette.testclient import TestClient
from src.global_config import env
from src.main import app


@pytest.fixture(scope='session')
def anyio_backend():
  return 'asyncio'

@pytest.fixture(scope='session', autouse=True)
def client():
  with TestClient(app=app, base_url='http://localhost:8000') as client:
    logging.error('Client is ready')
    yield client


@pytest.fixture(scope='session', autouse=True)
def db_engine():
    engine = create_engine(env.DATABASE_URL)
    # Create the database engine
    yield engine
    # Log the time taken for the drop tables operation
    start_time = time.time()
    engine.dispose()  
    try:
        with create_engine(env.DATABASE_URL.rsplit('/', 1)[0], isolation_level="AUTOCOMMIT").connect() as connection:
            # Terminate all connections to the database
            connection.execute(text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{env.DATABASE_NAME}'
                AND pid <> pg_backend_pid();
            """))
            # Drop the database
            # connection.execute(text(f"DROP DATABASE {env.DATABASE_NAME}"))
    except Exception as e:
        logging.error(f"Force drop database error: {e}")
    end_time = time.time()
    logging.info(f"Time taken to drop all tables: {end_time - start_time} seconds")
