from secrets import token_urlsafe

from graphql import GraphQLError
from global_config import ScopedSession, convert_keys_to_camel_case, DBSession
from licenses.http.validation import LicenseInput
from assets.db_models.asset_license import AssetLicenseModel


class LicenseService:
    def __init__(self):
        pass

    def create_license(self, license_input: LicenseInput):
        with ScopedSession() as session:
            asset_path = token_urlsafe(16)

            license = AssetLicenseModel(
                asset_id=license_input.assetId,
                level=license_input.level,
                permissions=license_input.permissions,
            )
            session.add(license)
            session.commit()
            session.flush()
            license = (
                DBSession.query(AssetLicenseModel).filter_by(id=license.id).first()
            )

            return {
                **convert_keys_to_camel_case(license.to_dict()),
                "assetPath": asset_path,
            }

    def get_license(self, l_id, session=DBSession):
        return session.query(AssetLicenseModel).filter_by(id=l_id).first()

    async def revoke_license(self, license_id: int):
        with ScopedSession() as session:
            try:
                license = self.get_license(license_id, session=session)

                if license is None:
                    raise GraphQLError("License not found")

                session.delete(license)
                session.commit()
                return "License revoked {}".format(license_id)
            except Exception as e:
                print(e)
                return "Failed to revoke license {}".format(license_id)
            finally:
                session.close()
