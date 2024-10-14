import pytest

from authentication.tests.auth_test import TestAuthenticationController
from event_archive.db_models.event import EventModel
from global_config.database import ScopedSession
from assets.db_models.asset import AssetModel
from src.main import app
from global_config import JWT_HEADER_NAME, DBSession
from stages.db_models.parent_stage import ParentStageModel
from stages.db_models.stage_attribute import StageAttributeModel
from users.db_models.user import PLAYER, SUPER_ADMIN
from stages.db_models.stage import StageModel
from stages.http.schema import stage_graphql_app

app.mount("/stage_graphql", stage_graphql_app)
test_AuthenticationController = TestAuthenticationController()


@pytest.mark.anyio
class TestStageController:
    async def test_01_create_stage(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)

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
                "config": None,
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

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        response = response.json()
        return response["data"]["createStage"]

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
                "config": None,
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

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        return response.json()

    async def test_02_update_stage(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        stage = DBSession.query(StageModel).first()
        response = self.update_stage(client, stage.id, data)
        assert "errors" not in response
        return response

    async def test_03_update_stage_failed(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        response = self.update_stage(client, 1000, data)
        assert "errors" in response

    async def duplicate_stage(self, client, id: int, data):
        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {"id": id, "name": "Duplicate Stage"}

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
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        return response.json()

    async def test_04_duplicate_stage_failed_with_wrong_id(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        response = await self.duplicate_stage(client, 1000, data)
        assert "errors" in response

    async def test_05_duplicate_stage(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        from stages.tests.test_media import TestMediaController

        test_MediaController = TestMediaController()
        asset_id = await test_MediaController.test_03_upload_media(client)

        with ScopedSession() as session:
            stage = DBSession.query(StageModel).first()
            item = ParentStageModel(stage_id=stage.id, child_asset_id=asset_id)
            session.add(item)
            session.commit()
            session.flush()

            response = await self.duplicate_stage(client, stage.id, data)
            assert "errors" not in response

    def remove_media(self, client, id: int, data):
        headers = {
            "Authorization": f'Bearer {data["data"]["login"]["access_token"]}',
            JWT_HEADER_NAME: data["data"]["login"]["refresh_token"],
        }

        variables = {"id": id}

        query = """
            mutation deleteStage($id: ID!) {
                deleteStage(id: $id) {
                        success
                }
            }
        """
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        return response.json()

    async def test_06_delete_stage_failed_with_wrong_id(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        response = self.remove_media(client, 1000, data)
        assert "errors" in response

    async def test_07_delete_stage_wrong_role(self, client):
        data = await test_AuthenticationController.test_player_login_successfully(
            client
        )
        stage = DBSession.query(StageModel).first()
        response = self.remove_media(client, stage.id, data)
        assert "errors" in response

    async def test_08_delete_stage(self, client):
        data = await test_AuthenticationController.test_02_login_successfully(client)
        stage = DBSession.query(StageModel).first()
        response = self.remove_media(client, stage.id, data)
        assert response["data"]["deleteStage"]["success"] == True

    async def sweep_stage(self, client, id: int):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": id}
        query = """
        mutation sweepStage($id: ID!) {
            sweepStage(id: $id) {
                    success
                    performanceId
            }
        }
        """
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        return response.json()

    async def test_09_sweep_stage_not_found(self, client):
        response = await self.sweep_stage(client, 1000)
        assert "errors" in response
        assert response["errors"][0]["message"] == "Stage not found"

    async def test_10_sweep_stage(self, client):
        stage = DBSession.query(StageModel).all()[-1]
        response = await self.sweep_stage(client, stage.id)
        assert response["errors"][0]["message"] == "The stage is already sweeped!"

    async def test_11_sweep_stage_successfully(self, client):
        stage = DBSession.query(StageModel).all()[-1]
        with ScopedSession() as session:
            event = EventModel(
                topic="/{}/".format(stage.file_location),
                mqtt_timestamp=1630000000,
                payload={"key": "value"},
            )
            session.add(event)
            session.commit()
            session.flush()
        response = await self.sweep_stage(client, stage.id)
        assert response["data"]["sweepStage"]["success"] == True
        assert response["data"]["sweepStage"]["performanceId"] is not None

    async def test_12_update_status_failed(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": 1000}
        query = """ 
            mutation updateStatus($id: ID!) {
                updateStatus(id: $id) {
                    result
                }
            }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert response.json()["errors"][0]["message"] == "Stage not found"

        headers = test_AuthenticationController.get_headers(client, PLAYER)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert (
            response.json()["errors"][0]["message"]
            == "You are not authorized to update this stage"
        )

    async def test_13_update_status(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        query = """ 
            mutation updateStatus($id: ID!) {
                updateStatus(id: $id) {
                    result
                }
            }
        """
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateStatus"]["result"] == "live"

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateStatus"]["result"] == "rehearsal"

        with ScopedSession() as session:
            status = (
                session.query(StageAttributeModel)
                .filter(
                    StageAttributeModel.stage_id == stage.id,
                    StageAttributeModel.name == "status",
                )
                .all()
            )
            session.delete(status[0])
            session.commit()
            session.flush()

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateStatus"]["result"] == "live"

    async def test_14_update_visibility_failed(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": 1000}
        query = """ 
            mutation updateVisibility($id: ID!) {
                updateVisibility(id: $id) {
                    result
                }
            }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert response.json()["errors"][0]["message"] == "Stage not found"

        headers = test_AuthenticationController.get_headers(client, PLAYER)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert (
            response.json()["errors"][0]["message"]
            == "You are not authorized to update this stage"
        )

    async def test_15_update_visibility(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        query = """ 
            mutation updateVisibility($id: ID!) {
                updateVisibility(id: $id) {
                    result
                }
            }
        """
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateVisibility"]["result"] == ""

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateVisibility"]["result"] == "true"

        with ScopedSession() as session:
            status = (
                session.query(StageAttributeModel)
                .filter(
                    StageAttributeModel.stage_id == stage.id,
                    StageAttributeModel.name == "visibility",
                )
                .first()
            )
            session.delete(status)
            session.commit()
            session.flush()

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateVisibility"]["result"] == "true"

    async def test_16_update_last_access_failed(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": 1000}
        query = """ 
            mutation updateLastAccess($id: ID!) {
                updateLastAccess(id: $id) {
                    result
                }
            }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert response.json()["errors"][0]["message"] == "Stage not found"

        headers = test_AuthenticationController.get_headers(client, PLAYER)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" in response.json()
        assert (
            response.json()["errors"][0]["message"]
            == "You are not authorized to update this stage"
        )

    async def test_17_update_last_access(self, client):
        headers = test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        stage = DBSession.query(StageModel).all()[-1]
        variables = {"id": stage.id}
        query = """ 
            mutation updateLastAccess($id: ID!) {
                updateLastAccess(id: $id) {
                    result
                }
            }
        """
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        assert "errors" not in response.json()
        assert response.json()["data"]["updateLastAccess"]["result"] is not None
