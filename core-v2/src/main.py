import glob
import importlib
import os
import sys

# Always on top
app_dir = os.path.abspath(os.path.dirname(__file__))
if app_dir not in sys.path:
    sys.path.append(app_dir)

from config.schema import config_graphql_endpoints
from core.middlewares.middleware import add_cors_middleware
from bootstraps import Bootstrap, app


def load_module(path: str):
    modules = glob.glob(path, recursive=True)
    for module in modules:
        importlib.import_module(
            module.replace(".py", "")
            .replace(".graphql", "")
            .replace("/", ".")
            .replace("src.", ""),
            package=None,
        )


load_module("*/*/entities/*.py")
load_module("*/*/schemas/*.py")
load_module("*/core/*/*.py")
load_module("*/core/*/*.py")
load_module("*/core/exceptions/*.py")
load_module("*/*/scripts/*.py")
load_module("*/*/graphql/*.py")
load_module("*/*/http/controllers/*.py")
load_module("*/config/*.py")


def start_app():
    bootstrap = Bootstrap(app)
    add_cors_middleware(app)
    config_graphql_endpoints(app)
    bootstrap.init_exception()


start_app()
