import base64
import pytest
from assets.entities.asset import AssetEntity
from authentication.tests.auth_test import TestAuthenticationController
from bootstraps import app
from assets.http.asset import asset_graphql_app
from config.database import DBSession
from config.env import JWT_HEADER_NAME


def load_base64_from_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded


app.mount("/asset_graphql", asset_graphql_app)
test_AuthenticationController = TestAuthenticationController()


@pytest.mark.anyio
class TestAssetController:
    mutation_query = """
        mutation UploadFile($base64: String!, $filename: String!) {
            uploadFile(base64: $base64, filename: $filename) {
                url
            }
        }
    """

    async def test_01_upload_file_successfully(self, client):
        data = await test_AuthenticationController.test_login_successfully(client)

        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {
            "base64": f"data:image/jpeg;base64,{load_base64_from_image('src/assets/tests/images/test.png')}",
            "filename": "test.png",
        }
        response = client.post(
            "/asset_graphql",
            json={"query": self.mutation_query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "uploadFile" in data["data"]
        assert "url" in data["data"]["uploadFile"]
        assert data["data"]["uploadFile"]["url"] is not None

    async def test_02_upload_file_without_authentication(self, client):
        variables = {
            "base64": f"data:image/jpeg;base64,{load_base64_from_image('src/assets/tests/images/test.png')}",
            "filename": "test.png",
        }
        response = client.post(
            "/asset_graphql",
            json={"query": self.mutation_query, "variables": variables},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "errors" in data
        assert data["errors"][0]["message"] == "Authenticated Failed"

    async def test_03_save_media_successfully(self, client):
        data = await test_AuthenticationController.test_login_successfully(client)

        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        mutation_query = """
            mutation SaveMedia($input: SaveMediaInput!) {
                saveMedia(input: $input) {
                    asset {
                        id
                    }
                }
            }
        """

        variables = {
            "input": {
                "name": "test",
                "mediaType": "image",
                "urls": ["https://test.com/test.png"],
                "w": 100,
                "h": 100,
                "tags": ["test"],
                "copyrightLevel": 0,
                "stageIds": [],
                "userIds": [],
                "owner": data["data"]["login"]["username"],
            }
        }
        response = client.post(
            "/asset_graphql",
            json={"query": mutation_query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "saveMedia" in data["data"]
        assert "id" in data["data"]["saveMedia"]["asset"]

    async def test_04_save_media_without_authentication(self, client):
        mutation_query = """
            mutation SaveMedia($input: SaveMediaInput!) {
                saveMedia(input: $input) {
                    asset {
                        id
                    }
                }
            }
        """

        variables = {
            "input": {
                "name": "test",
                "mediaType": "image",
                "urls": ["https://test.com/test.png"],
                "w": 100,
                "h": 100,
                "tags": ["test"],
                "copyrightLevel": 0,
                "stageIds": [],
                "userIds": [],
                "owner": "test",
            }
        }
        response = client.post(
            "/asset_graphql",
            json={"query": mutation_query, "variables": variables},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "errors" in data
        assert data["errors"][0]["message"] == "Authenticated Failed"

    async def test_05_search_assets(self, client):
        data = await test_AuthenticationController.test_login_successfully(client)

        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        query = """
            query {
                media(input: {limit: 10, page: 1}) {
                    totalCount
                    edges {
                        id
                        name
                    }
                }
            }
        """

        response = client.post(
            "/asset_graphql",
            json={"query": query},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "media" in data["data"]
        assert "totalCount" in data["data"]["media"]
        assert "edges" in data["data"]["media"]
        assert len(data["data"]["media"]["edges"]) > 0

    async def test_06_delete_media(self, client):
        asset = DBSession.query(AssetEntity).first()
        data = await test_AuthenticationController.test_login_successfully(client)

        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        mutation_query = """
            mutation DeleteMedia($id: ID!) {
                deleteMedia(id: $id) {
                    success
                }
            }
        """

        variables = {"id": asset.id}
        response = client.post(
            "/asset_graphql",
            json={"query": mutation_query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200

        asset = DBSession.query(AssetEntity).filter_by(id=asset.id).first()
        assert asset is None

    async def test_07_delete_media_without_authentication(self, client):
        mutation_query = """
            mutation DeleteMedia($id: ID!) {
                deleteMedia(id: $id) {
                    success
                }
            }
        """

        variables = {"id": 1}
        response = client.post(
            "/asset_graphql",
            json={"query": mutation_query, "variables": variables},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "errors" in data
        assert data["errors"][0]["message"] == "Authenticated Failed"
