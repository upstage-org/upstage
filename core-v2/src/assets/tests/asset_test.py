import base64
import pytest
from authentication.tests.auth_test import TestAuthenticationController
from bootstraps import app
from assets.http.asset import asset_graphql_app
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

    async def test_upload_file_successfully(self, client):
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

    async def test_upload_file_without_authentication(self, client):
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
