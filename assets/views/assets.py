import logging

from flask import Flask, Blueprint, jsonify, request, url_for, send_file

from ..system import create_asset, get_asset, save_file, access


blueprint = Blueprint("assets", __name__)


@blueprint.route("/", methods=["POST"])
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
            logging.error(e)
            return "Internal error", 500
    else:
        return "Name or description not specified", 400


@blueprint.route("/<string:path>", methods=["GET"])
def access_asset(path):
    file_location = access(path)
    if file_location:
        return send_file(file_location)
    else:
        return "Not Found", 404
