from fastapi import FastAPI
from fastapi_exception import FastApiException


class Bootstrap:
    def __init__(self, app: FastAPI):
        self.app = app

    def init_exception(self):
        FastApiException.config()
