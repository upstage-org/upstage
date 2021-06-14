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
from licenses.models import StageLicense, AssetLicense

def create_license(**kwargs):
    app.logger.info(f"Attempting to create license: {kwargs.items()}")
    kwargs["access_path"] = token_urlsafe(16)
    new_license = AssetLicense(**kwargs)
    try:
        with ScopedSession as local_db_session:
            local_db_session.add(new_license)
            local_db_session.flush()
            app.logger.info(f"License created: {new_license.id}")
    except Exception as e:
        app.logger.error(f"Failed to create license {e}")
        new_license = None
    return new_license


def get_license(**kwargs):
    return AssetLicense.query.filter_by(**kwargs).first()

def access(path):
    app.logger.info(f"Attempt to access license: {path}")
    lic = get_license(access_path=path)
    if lic:
        if lic.expires_on > datetime.utcnow():
            app.logger.info(f"License is valid: {lic.id}")
            return os.path.abspath(lic.asset.file_location)
        else:
            app.logger.info(f"License has expired:  {lic.id}")
            try:
                with ScopedSession as local_db_session:
                    local_db_session.query(Asset).filter_by(id=lic.id).delete()
                    app.logger.info(f"License has been removed: {lic.id}")
            except Exception as e:
                app.logger.warning(f"Failed to remove expired license {lic.id}: {e}")
    return None


def revoke_license(**kwargs):
    lic = get_license(**kwargs)
    if lic:
        app.logger.info(f"Revoking license: {lic}")
        try:
            with ScopedSession as local_db_session:
                local_db_session.query(AssetLicense).filter_by(id=lic.id).delete()
            app.logger.info(f"{lic} revoked")
            return True
        except Exception as e:
            app.logger.error(f"Error revoking {lic}: {e}")
            return False
    else:
        app.logger.warn(f"Refusing to attempt to revoke non-existent license: {kwargs}")
        return False
