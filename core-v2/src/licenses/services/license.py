from secrets import token_urlsafe
from global_config import ScopedSession, convert_keys_to_camel_case
from licenses.http.validation import LicenseInput
from assets.db_models.asset_license import AssetLicenseModel



class LicenseService:
    def __init__(self):
        pass

    def create_license(self, license_input: LicenseInput):
        with ScopedSession as session:
            asset_path = token_urlsafe(16)

            license = AssetLicenseModel(
                asset_id=license_input.assetId,
                level=license_input.level,
                permissions=license_input.permissions,
            )

            session.add(license)
            session.commit()
            session.flush()

            return {**convert_keys_to_camel_case(license), "assetPath": asset_path}

    def get_license(self, **kwargs):
        with ScopedSession as session:
            return session.query(AssetLicenseModel).filter_by(**kwargs).first()
