from fastapi import FastAPI
from fastapi_exception import FastApiException
from fastapi_global_variable import GlobalVariable
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from global_config import ENV_TYPE, config_graphql_endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def add_cors_middleware(app):
    if ENV_TYPE == "Production":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


class Bootstrap:
    def __init__(self, app: FastAPI):
        self.app = app

    def init_exception(self):
        FastApiException.config()


def start_app():
    bootstrap = Bootstrap(app)
    add_cors_middleware(app)
    config_graphql_endpoints(app)
    bootstrap.init_exception()


app = FastAPI(title="upstage", lifespan=lifespan)
GlobalVariable.set("app", app)

start_app()
