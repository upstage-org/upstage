from config.env import (
    EMAIL_TIME_EXPIRED_TOKEN,
    MONGO_EMAIL_DB,
    MONGO_EMAIL_HOST,
    MONGO_EMAIL_PORT,
    MONGO_HOST,
    MONGO_PORT,
    MONGODB_COLLECTION_TOKEN,
)
import pymongo


def build_mongo_client(host=MONGO_HOST, port=MONGO_PORT):
    return pymongo.MongoClient(host, port)


def build_mongo_email_client(host=MONGO_EMAIL_HOST, port=MONGO_EMAIL_PORT):
    return pymongo.MongoClient(host, port)


def get_mongo_token_collection():
    client = build_mongo_email_client()
    mongo_db = client[MONGO_EMAIL_DB]
    collection = mongo_db[MONGODB_COLLECTION_TOKEN]
    if "expired_date" not in collection.index_information():
        collection.create_index(
            "expired_date",
            name="expired_date",
            expireAfterSeconds=EMAIL_TIME_EXPIRED_TOKEN,
        )
    return collection
