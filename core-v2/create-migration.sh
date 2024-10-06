# alembic revision -m "Create Tag Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Asset Type Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Asset Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Asset License Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Asset Atribute Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Asset Usage Table"  --version-path=src/assets/databases/migrations
# alembic revision -m "Create Media Tag Table"  --version-path=src/assets/databases/migrations


# alembic revision -m "Create Stage Table"  --version-path=src/stages/databases/migrations
# alembic revision -m "Create Stage Attribute Table"  --version-path=src/stages/databases/migrations
# alembic revision -m "Create Parent Stage Table"  --version-path=src/stages/databases/migrations

# alembic revision -m "Create Config Table"  --version-path=src/setting/databases/migrations

# alembic revision -m "Create Event Table"  --version-path=src/event_archive/databases/migrations


alembic revision -m "Create Connection Stat Table"  --version-path=src/upstage_stats/db_migrations
alembic revision -m "Create Receive Stat Table"  --version-path=src/upstage_stats/db_migrations