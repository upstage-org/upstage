from datetime import datetime, timedelta
from graphene.test import Client
from flask import request
from core import app
from core.studio.schema import studio_schema
from . import get_access_token


def test_last_login():
    with app.test_request_context():
        client = Client(studio_schema)
        request.headers = {"X-Access-Token": get_access_token()}

        executed = client.execute(
            """
            query {
                adminPlayers {
                    edges {
                        node {
                            username
                            lastLogin
                        }
                    }
                }
            }
            """
        )
        assert "errors" not in executed
        assert "data" in executed
        # automation_test should have logged in recently by the call of get_access_token()
        automation_test = [
            x
            for x in executed["data"]["adminPlayers"]["edges"]
            if x["node"]["username"] == "automation_test"
        ]
        assert len(automation_test) == 1
        assert automation_test[0]["node"]["lastLogin"] is not None
        assert datetime.strptime(
            automation_test[0]["node"]["lastLogin"], "%Y-%m-%dT%H:%M:%S.%f"
        ) > datetime.now() - timedelta(
            minutes=1
        )  # should be within 1 minute
