export PGPASSWORD="postgres"
psql -h localhost -p 5437 -U postgres -c "DROP DATABASE IF EXISTS up_test;"
psql -h localhost -p 5437 -U postgres -c "CREATE DATABASE up_test;"
alembic upgrade head
coverage run -m pytest
psql -h localhost -p 5437 -U postgres -c "DROP DATABASE IF EXISTS up_test;"


# -k TestStudioController