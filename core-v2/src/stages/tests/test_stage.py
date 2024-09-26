import pytest

from authentication.tests.auth_test import TestAuthenticationController
from bootstraps import app
from config.database import DBSession
from config.env import JWT_HEADER_NAME
from stages.entities.stage import StageEntity
from stages.http.stage import stage_graphql_app

app.mount("/stage_graphql", stage_graphql_app)
test_AuthenticationController = TestAuthenticationController()

@pytest.mark.anyio
class TestStageController:
    async def test_01_create_stage(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)

        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {
            "input": {
                "fileLocation": "path/to/file",
                "status": "active",
                "visibility": True,
                "cover": "http://example.com/cover.jpg",
                "name": "Stage Name",
                "description": "Description of the stage",
                "playerAccess": "public",
                "config": None
            }
        }

        query = """
            mutation createStage($input: StageInput!) {
                createStage(input: $input) {
                        id
                        name
                        description
                        fileLocation
                        cover
                        visibility
                }
            }
        """

        response = client.post("/stage_graphql", json={"query": query, "variables": variables}, headers=headers)
        assert response.status_code == 200
        assert "errors"  not in response.json()

    def update_stage(self, client, id: int, data):
        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {
            "input": {
                "id": id,
                "fileLocation": "path/to/file",
                "status": "active",
                "visibility": True,
                "cover": "http://example.com/cover.jpg",
                "name": "Stage Name",
                "description": "Description of the stage",
                "playerAccess": "public",
                "config": None
            }
        }

        query = """
            mutation updateStage($input: StageInput!) {
                updateStage(input: $input) {
                        id
                        name
                        description
                        fileLocation
                        cover
                        visibility
                }
            }
        """

        response = client.post("/stage_graphql", json={"query": query, "variables": variables}, headers=headers)
        assert response.status_code == 200
        return response.json()


    async def test_02_update_stage(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        stage = DBSession.query(StageEntity).first()
        response = self.update_stage(client, stage.id, data)
        assert "errors"  not in response

    async def test_03_update_stage_failed(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        response = self.update_stage(client, 10, data)
        assert "errors" in response

    def duplicate_stage(self, client, id: int, data):
        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {
            "id": id,
            "name": "Duplicate Stage"
        }

        query = """
            mutation duplicateStage($id: ID!, $name: String!) {
                duplicateStage(id: $id, name: $name) {
                        id
                        name
                        description
                        fileLocation
                        cover
                        visibility
                }
            }
        """
        response = client.post("/stage_graphql", json={"query": query, "variables": variables}, headers=headers)
        assert response.status_code == 200
        return response.json()


    async def test_04_duplicate_stage_failed_with_wrong_id(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        response = self.duplicate_stage(client, 10, data)
        assert "errors" in response
    
    async def test_05_duplicate_stage(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        stage = DBSession.query(StageEntity).first()
        response = self.duplicate_stage(client, stage.id, data)
        assert "errors"  not in response


    def remove_media(self, client, id: int, data):
        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {
            "id": id
        }

        query = """
            mutation deleteStage($id: ID!) {
                deleteStage(id: $id) {
                        success
                }
            }
        """
        response = client.post("/stage_graphql", json={"query": query, "variables": variables}, headers=headers)
        assert response.status_code == 200
        return response.json()


    async def test_06_delete_stage_failed_with_wrong_id(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        response = self.remove_media(client, 10, data)
        assert "errors" in response

    async def test_07_delete_stage_wrong_role(self, client):
        data  = await test_AuthenticationController.test_player_login_successfully(client)
        stage = DBSession.query(StageEntity).first()
        response = self.remove_media(client, stage.id, data)
        assert "errors" in response

    async def test_08_delete_stage(self, client):
        data  = await test_AuthenticationController.test_02_login_successfully(client)
        stage = DBSession.query(StageEntity).first()
        response = self.remove_media(client, stage.id, data)
        assert response["data"]["deleteStage"]["success"] == True 

     