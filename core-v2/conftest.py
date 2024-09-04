import logging
import pytest
from starlette.testclient import TestClient
from bootstraps import app

@pytest.fixture(scope='session')
def anyio_backend():
  return 'asyncio'

@pytest.fixture(scope='session', autouse=True)
def client():
  with TestClient(app=app, base_url='http://test') as client:
    logging.error('Client is ready')
    yield client
