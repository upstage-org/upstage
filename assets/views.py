import logging

from flask import Flask, Blueprint, jsonify, request, url_for, send_file

from .system import create_asset, get_asset, create_license, save_file, access, revoke_license

assets = Blueprint("assets", __name__, url_prefix="/assets")
licenses = Blueprint("licenses", __name__, url_prefix="/assets/<int:asset_id>/licenses")


@assets.route("/", methods=["POST"])
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


@assets.route("/<string:path>", methods=["GET"])
def access_asset(path):
    file_location = access(path)
    if file_location:
        return send_file(file_location)
    else:
        return "Not Found", 404


@licenses.before_request
def before_licenses():
    asset = get_asset(id=request.view_args["asset_id"])
    if not asset:
        return f"Asset with ID: {request.view_args['asset_id']} does not exist", 404


@licenses.route("/", methods=["POST"])
def licenses_create(asset_id):
    if request.is_json:
        request.json["asset_id"] = asset_id
        try:
            new_license = create_license(**request.json)
            return (
                jsonify(
                    {
                        "id": new_license.id,
                        "expires_on": new_license.expires_on,
                        "access_path": url_for(
                            "assets.access_asset", path=new_license.access_path
                        ),
                    }
                ),
                200,
            )
        except Exception as e:
            logging.error(e)
            return jsonify(e), 400
    else:
        return "Request must be in JSON format", 400


@licenses.route("/<int:id>", methods=["DELETE"])
def licenses_revoke(asset_id, id):
    if revoke_license(id=id):
        return f"License revoked: {id}", 200
    else:
        return f"Failed to revoke: {id}", 500


app = Flask(__name__)
app.register_blueprint(assets)
app.register_blueprint(licenses)
