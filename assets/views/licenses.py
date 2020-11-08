import logging

from flask import Flask, Blueprint, jsonify, request, url_for

from ..system import get_asset, create_license, revoke_license


blueprint = Blueprint(
    "licenses", __name__, url_prefix="/<int:asset_id>/licenses"
)


@blueprint.before_request
def before_licenses():
    asset = get_asset(id=request.view_args["asset_id"])
    if not asset:
        return f"Asset with ID: {request.view_args['asset_id']} does not exist", 404


@blueprint.route("/", methods=["POST"])
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


@blueprint.route("/<int:id>", methods=["DELETE"])
def licenses_revoke(asset_id, id):
    if revoke_license(id=id):
        return f"License revoked: {id}", 200
    else:
        return f"Failed to revoke: {id}", 500
