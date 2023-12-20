import os
import sys
import unittest
import pprint

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.asset.models import AssetType, Asset
from core.asset.system import create_asset_type, create_asset


class Testing(unittest.TestCase):
    def test_create_asset_type(self):
        asset_type = create_asset_type(
            name="Avatar",
            description="Character/thing that can move and do things",
            file_location="/some/location",
        )
        assert asset_type != None
        pprint.pprint(asset_type)


if __name__ == "__main__":
    unittest.main()
