#!/usr/bin/env bash

docker-compose up -d

# Wait for the database to be ready
echo "Waiting for container to be ready..."
sleep 3

until docker exec combined-services pg_isready -U postgres &>/dev/null; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "PostgreSQL is ready!"

docker exec -d combined-services mongod --config /etc/mongod.conf &

until curl -s localhost:27017 &>/dev/null; do
    echo "Waiting for MongoDB to be ready..."
    sleep 2
done

echo "MongoDB is ready!"

docker exec -d combined-services mosquitto -c /etc/mosquitto/mosquitto.conf &

until nc -zv localhost 1883 &>/dev/null; do
    echo "Waiting for Mosquitto to be ready..."
    sleep 2
done

echo "Mosquitto is ready!"


until nc -zv localhost 3000 &>/dev/null; do
    echo "Waiting for port 3000 to be ready..."
    sleep 2
done

echo "Application is ready!"

docker exec -d upstage_app /bin/bash -c "TIMESTAMP=$(date +%d_%m_%Y) python3 -m scripts.run_upstage_email > upstage_email.log 2>&1 &"
docker exec -d upstage_app /bin/bash -c "TIMESTAMP=$(date +%d_%m_%Y) python3 -m scripts.run_event_archive > event_archive.log 2>&1 &"
docker exec -d upstage_app /bin/bash -c "TIMESTAMP=$(date +%d_%m_%Y) python3 -m scripts.run_upstage_stats > upstage_stats.log 2>&1 &"

echo "Timestamp is ready!"
