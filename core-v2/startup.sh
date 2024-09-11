cp .env.example .env
alembic upgrade head
ruff format src
uvicorn src.main:app --reload