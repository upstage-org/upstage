# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.project_globals import app
from config import URL_PREFIX

from flask import jsonify, request, url_for, send_file
from core.asset.system import (
    create_asset,
    one_asset,
    all_assets,
    save_file,
    update_asset,
    remove_asset,
)

BASE_URL = "/{0}asset".format(URL_PREFIX)


def marshall(asset):
    return {
        "id": asset.id,
        "name": asset.name,
        "description": asset.description,
        "created_on": asset.created_on,
    }


@app.route(f"{BASE_URL}/", methods=["POST"])
def assets_create():
    if all([x in request.form for x in ["name", "description"]]):
        if "file" not in request.files:
            return "File not provided", 400
        req_file = request.files["file"]
        if req_file.filename == "":
            return "No file selected", 400
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "file_location": save_file(req_file),
        }
        if data["file_location"] == None:
            return "Failed to save file", 500
        try:
            new_asset = create_asset(**data)
            return (
                jsonify(
                    {
                        "id": new_asset.id,
                        "name": new_asset.name,
                        "description": new_asset.description,
                    }
                ),
                200,
            )
        except Exception as e:
            app.logger.error(e)
            return "Internal error", 500
    else:
        return "Name or description not specified", 400


@app.route(f"{BASE_URL}/", methods=["GET"])
def assets_list():
    assets = all_assets()
    output = []
    for a in assets:
        output.append(marshall(a))
    return jsonify(output)


@app.route(f"{BASE_URL}/<int:id>/", methods=["GET"])
def asset_get(id):
    asset = one_asset(id=id)
    if asset:
        return jsonify(marshall(asset)), 200
    else:
        return f"No asset with ID: {id}", 404


@app.route(f"{BASE_URL}/<int:id>", methods=["PATCH"])
def asset_update(id):
    asset = one_asset(id=id)
    if asset:
        data = request.form.marshall()
        if "file" in request.files:
            req_file = request.files["file"]
            if req_file.filename == "":
                return "No file selected", 400
            data["file_location"] = save_file(req_file)
            if data["file_location"] is None:
                del data["file_location"]
        if len(data.keys()):
            try:
                asset = update_asset(id, **data)
                return jsonify(marshall(asset))
            except Exception as e:
                app.logger.error(f"Failed to update asset {id} with {data}: {e}")
                return "Failed to update asset", 500
        else:
            return "No updatable attributes specified", 400
    else:
        return f"No asset with ID: {id}", 404


@app.route(f"{BASE_URL}/<int:id>", methods=["DELETE"])
def asset_remove(id):
    if remove_asset(id=id):
        return f"Asset removed: {id}", 200
    else:
        return f"Failed to remove asset: {id}", 500


@app.route(f"{BASE_URL}/<string:path>", methods=["GET"])
def asset_access(path):
    file_location = access(path)
    if file_location:
        return send_file(file_location)
    else:
        return "Not Found", 404
