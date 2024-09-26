cp .env.unit_test .env
export $(grep -v '^#' .env | xargs)

export PGPASSWORD=$DATABASE_PASSWORD
psql -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER -c "DROP DATABASE IF EXISTS $DATABASE_NAME;"
psql -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER -c "CREATE DATABASE $DATABASE_NAME;"
alembic upgrade head
coverage run -m pytest
psql -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER -c "DROP DATABASE IF EXISTS $DATABASE_NAME;"