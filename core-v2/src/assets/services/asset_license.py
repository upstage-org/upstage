from assets.db_models.asset_license import AssetLicenseModel


class AssetLicenseService:
    def __init__(self):
        pass

    def create(
        self, asset_id: int, copyright_level: str, player_access: str, local_db_session
    ):
        local_db_session.query(AssetLicenseModel).filter(
            AssetLicenseModel.asset_id == asset_id
        ).delete()

        asset_license = AssetLicenseModel(
            asset_id=asset_id,
            level=copyright_level,
            permissions=player_access,
        )
        local_db_session.add(asset_license)
        local_db_session.commit()
        local_db_session.refresh(asset_license)
        local_db_session.flush()
        return asset_license
