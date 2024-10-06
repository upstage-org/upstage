import pytest
from global_config import DBSession, ScopedSession, convert_keys_to_camel_case
from src.main import app
from performance_config.http.schema import performance_graphql_app

app.mount("/performance_graphql", performance_graphql_app)


@pytest.mark.anyio
class TestPerformanceConfig:
    async def test_01_get_performance_communication(self, client):
        query = """
            query PerformanceCommunication {
                performanceCommunication {
                    id
                    ownerId
                } 

            }
        """
        response = client.post("/performance_graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "performanceCommunication" in data["data"]
        assert data["data"]["performanceCommunication"] is not None

    async def test_02_get_performance_config(self, client):
        query = """
            query PerformanceConfig {
                performanceConfig {
                    id
                    ownerId
                } 

            }
        """
        response = client.post("/performance_graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "performanceConfig" in data["data"]
        assert data["data"]["performanceConfig"] is not None

    async def test_03_get_scene(self, client):
        query = """
            query Scene {
                scene {
                    id
                    ownerId
                } 

            }
        """
        response = client.post("/performance_graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "scene" in data["data"]
        assert data["data"]["scene"] is not None

    async def test_04_get_parent_stage(self, client):
        query = """
            query ParentStage {
                parentStage {
                    id
                    stageId
                } 

            }
        """
        response = client.post("/performance_graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert "data" in data
        assert "parentStage" in data["data"]
        assert data["data"]["parentStage"] is not None
