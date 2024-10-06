import pytest
from authentication.tests.auth_test import TestAuthenticationController
from global_config import DBSession, ScopedSession
from event_archive.db_models.event import EventModel
from src.main import app
from performance_config.db_models.performance import PerformanceModel
from stages.db_models.stage import StageModel
from users.db_models.user import PLAYER, SUPER_ADMIN
from stages.tests.test_stage import TestStageController
from stages.http.schema import stage_graphql_app

app.mount("/stage_graphql", stage_graphql_app)
test_AuthenticationController = TestAuthenticationController()
test_StageController = TestStageController()


@pytest.mark.anyio
class TestPerformanceController:
    stage = None

    async def test_01_start_recording(self, client):
        stage = await test_StageController.test_01_create_stage(client)
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {
            "input": {"stageId": stage["id"], "name": "Test", "description": "Test"}
        }

        query = """
            mutation startRecording($input: RecordInput!) {
                startRecording(input: $input) {
                    id
                    }
                }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "startRecording" in data["data"]
        assert data["data"]["startRecording"] is not None

    async def test_02_start_recording_failed(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"input": {"stageId": 1000, "name": "Test", "description": "Test"}}

        query = """
            mutation startRecording($input: RecordInput!) {
                startRecording(input: $input) {
                    id
                    }
                }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert data["errors"][0]["message"] == "Stage not found"

        stage = await test_StageController.test_01_create_stage(client)
        variables = {
            "input": {"stageId": stage["id"], "name": "Test", "description": "Test"}
        }

        headers = await test_AuthenticationController.get_headers(client, PLAYER)
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert (
            data["errors"][0]["message"]
            == "You are not allowed to record for this stage"
        )

    async def test_03_update_recording(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        stage = await test_StageController.test_01_create_stage(client)
        variables = {
            "input": {"stageId": stage["id"], "name": "Test", "description": "Test"}
        }

        query = """
            mutation startRecording($input: RecordInput!) {
                startRecording(input: $input) {
                    id
                    }
                }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "startRecording" in data["data"]
        assert data["data"]["startRecording"] is not None

        performance = data["data"]["startRecording"]
        variables = {
            "input": {"id": performance["id"], "name": "Test", "description": "Test"}
        }

        query = """
            mutation updatePerformance($input: PerformanceInput!) {
                updatePerformance(input: $input) {
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
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "updatePerformance" in data["data"]
        assert data["data"]["updatePerformance"] is not None

    async def test_04_update_recording_failed(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"input": {"id": 1000, "name": "Test", "description": "Test"}}

        query = """
            mutation updatePerformance($input: PerformanceInput!) {
                updatePerformance(input: $input) {
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
        data = response.json()
        assert "errors" in data
        assert data["errors"][0]["message"] == "Performance not found"

        performance = DBSession.query(PerformanceModel).first()
        variables = {
            "input": {
                "id": performance.id,
                "name": "Test",
                "description": "Test",
            }
        }

        headers = await test_AuthenticationController.get_headers(client, PLAYER)
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert (
            data["errors"][0]["message"]
            == "You are not allowed to update this performance"
        )

    async def test_05_save_recording(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        performance = DBSession.query(PerformanceModel).first()
        variables = {"id": performance.id}

        query = """
            mutation saveRecording($id: ID!) {
                saveRecording(id: $id) {
                        id
                    }
                }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert data["errors"][0]["message"] == "Nothing to record!"

        stage = DBSession.query(StageModel).filter_by(id=performance.stage_id).first()
        with ScopedSession() as session:
            event = EventModel(
                topic="/{}/".format(stage.file_location),
                mqtt_timestamp=1630000000,
                payload={"key": "value"},
            )
            session.add(event)
            session.commit()
            session.flush()

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "saveRecording" in data["data"]
        assert data["data"]["saveRecording"] is not None

    async def test_06_save_recording_failed(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": 1000}

        query = """
            mutation saveRecording($id: ID!) {
                saveRecording(id: $id) {
                        id
                    }
                }
        """

        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert data["errors"][0]["message"] == "Performance not found"

        performance = DBSession.query(PerformanceModel).first()
        variables = {"id": performance.id}

        headers = await test_AuthenticationController.get_headers(client, PLAYER)
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert (
            data["errors"][0]["message"]
            == "Only stage owner or Admin can save a recording!"
        )

    async def test_07_delete_performance(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        performance = DBSession.query(PerformanceModel).first()
        variables = {"id": performance.id}

        query = """
            mutation deletePerformance($id: ID!) {
                deletePerformance(id: $id) {
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
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "deletePerformance" in data["data"]
        assert data["data"]["deletePerformance"] is not None

    async def test_08_delete_performance_failed(self, client):
        headers = await test_AuthenticationController.get_headers(client, SUPER_ADMIN)
        variables = {"id": 1000}

        query = """
            mutation deletePerformance($id: ID!) {
                deletePerformance(id: $id) {
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
        data = response.json()
        assert "errors" in data
        assert data["errors"][0]["message"] == "Performance not found"

        performance = DBSession.query(PerformanceModel).first()
        variables = {"id": performance.id}

        headers = await test_AuthenticationController.get_headers(client, PLAYER)
        response = client.post(
            "/stage_graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert (
            data["errors"][0]["message"]
            == "You are not allowed to delete this performance"
        )
