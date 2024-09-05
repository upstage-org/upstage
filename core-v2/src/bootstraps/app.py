from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_global_variable import GlobalVariable


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="upstage", lifespan=lifespan)
GlobalVariable.set("app", app)

# if 'pytest' not in sys.modules and env.SENTRY_DNS:
#   sentry_sdk.init(dsn=env.SENTRY_DNS, traces_sample_rate=0.1)
