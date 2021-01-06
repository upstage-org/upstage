import logging
import secrets
import os
import sys

import pymongo

import config as conf


def build_client(host=conf.MONGO_HOST, port=conf.MONGO_PORT):
    return pymongo.MongoClient(host, port)
