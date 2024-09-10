cp .env.unit_test .env
alembic upgrade head
pytest
cp .env.example .env
alembic upgrade head
ruff format src
uvicorn src.main:app --reload