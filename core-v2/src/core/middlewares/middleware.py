from fastapi.middleware.cors import CORSMiddleware
from config.env import ENV_TYPE


def add_cors_middleware(app):
    if ENV_TYPE == "Production":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
