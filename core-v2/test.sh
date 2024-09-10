cp .env.unit_test .env
alembic upgrade head
pytest