from flask import Flask

from .assets import blueprint as assets
from .licenses import blueprint as licenses

app = Flask(__name__)
app.register_blueprint(assets)
app.register_blueprint(licenses)
