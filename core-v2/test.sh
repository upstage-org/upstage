cp .env.unit_test .env
alembic upgrade head
coverage run -m pytest