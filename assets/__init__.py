import os
import logging

from .views import app
from .data import db


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DB_URI", "postgresql://admin:password@localhost:5432/upstage"
)
app.config["UPLOAD_DIR"] = os.path.abspath(os.getenv("UPLOAD_DIR", "./uploads"))
if not os.path.isdir(app.config["UPLOAD_DIR"]):
    logging.info(f"{app.config['UPLOAD_DIR']} doesn't exist.  Creating...")
    os.makedirs(app.config["UPLOAD_DIR"])
db.init_app(app)
