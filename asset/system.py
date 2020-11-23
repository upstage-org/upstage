from datetime import datetime
import os
import sys
appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import time
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from config.project_globals import ScopedSession,app
from asset.models import Asset, AssetLicense

def save_file(file):
    filename = secure_filename(f"{time.time()}_{file.filename}")
    file_location = os.path.join(
        os.path.abspath(current_app.config["UPLOAD_DIR"]), filename
    )
    file.save(file_location)
    if not os.path.isfile(file_location):
        file_location = None
    return file_location


def create_asset(**kwargs):
    app.logger.info(f"Attempting to create asset: {kwargs.items()}")
    try:
        with ScopedSession as local_db_session:
            new_asset = Asset(**kwargs)
            local_db_session.add(new_asset)
            local_db_session.flush()
            app.logger.info(f"Asset created: {new_asset.id}")
    except:
        new_asset = None
    return new_asset


def create_asset_type(**kwargs):
    app.logger.info(f"Attempting to create asset type: {kwargs.items()}")
    try:
        with ScopedSession as local_db_session:
            new_asset_type = AssetType(**kwargs)
            local_db_session.add(new_asset_type)
            local_db_session.flush()
            app.logger.info(f"Asset type created: {new_asset.id}")
    except:
        new_asset_type = None
    return new_asset_type

def one_asset(**kwargs): return Asset.query.filter_by(**kwargs).first()


def all_assets(): return Asset.query.all()


def update_asset(id, **kwargs):
    for k in kwargs.keys():
        if k not in ["name", "description", "file_location"]:
            del kwargs[k]
    app.logger.info(f"Updating asset: {kwargs}")
    try:
        with ScopedSession as local_db_session:
            local_db_session.query(Asset).filter_by(id=id).update(kwargs)
            app.logger.info(f"Asset updated: {id}")
        return Asset.query.filter_by(id=id).first()
    except Exception as e:
        app.logger.error(f"Failed to update asset {id}: {e}")
        raise e


def remove_asset(**kwargs):
    asset = one_asset(**kwargs)
    if asset:
        app.logger.info(f"Removing asset: {asset}")
        try:
            with ScopedSession as local_db_session:
                local_db_session.query(Asset).filter_by(id=id).delete()
                app.logger.info(f"{asset} removed")
            return True
        except:
            return False
    else:
        app.logger.warn(f"Refusing to attempt to remove non-existent asset: {kwargs}")
        return False

