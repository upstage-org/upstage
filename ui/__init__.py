import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/<path:filename>", methods=["GET"])
def get_file(filename):
    real_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            filename
        )
    )
    if os.path.isfile(real_path):
        return send_file(real_path)
    else:
        return f"Not found", 404