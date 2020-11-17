# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import Flask, Blueprint, jsonify, request, url_for

from views import app
from assset.system import one_asset, create_license, revoke_license

blueprint = Blueprint("licenses", __name__, url_prefix="/<int:asset_id>/licenses")


@blueprint.before_request
def before_licenses():
    asset = one_asset(id=request.view_args["asset_id"])
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
                            "assets.asset_access", path=new_license.access_path
                        ),
                    }
                ),
                200,
            )
        except Exception as e:
            app.logger.error(e)
            return jsonify(e), 400
    else:
        return "Request must be in JSON format", 400


@blueprint.route("/<int:id>", methods=["DELETE"])
def licenses_revoke(asset_id, id):
    if revoke_license(id=id):
        return f"License revoked: {id}", 200
    else:
        return f"Failed to revoke: {id}", 500
