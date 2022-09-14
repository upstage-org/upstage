import logging
import os
import secrets
import sys

import pymongo
from config.settings import (EMAIL_TIME_EXPIRED_TOKEN, MONGO_DB, MONGO_HOST,
                             MONGO_PORT, MONGODB_COLLECTION_TOKEN,
                             SQLALCHEMY_DATABASE_URI)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def build_mongo_client(host=MONGO_HOST, port=MONGO_PORT):
    return pymongo.MongoClient(host, port)


def build_pg_engine(connection_string=SQLALCHEMY_DATABASE_URI):
    return create_engine(connection_string)


def build_pg_session():
    eng = build_pg_engine()
    Session = sessionmaker(bind=eng)
    return Session()


def get_mongo_token_collection():
    client = build_mongo_client()
    mongo_db = client[MONGO_DB]
    # queue = db[EVENT_COLLECTION]

    # mongo_connection = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/')
    # mongo_db = mongo_connection[MONGO_DB]
    collection = mongo_db[MONGODB_COLLECTION_TOKEN]
    if 'expired_date' in collection.index_information():
        collection.drop_index('expired_date')
    collection.create_index("expired_date", name="expired_date", expireAfterSeconds=EMAIL_TIME_EXPIRED_TOKEN)
    return collection
