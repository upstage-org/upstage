from graphene.test import Client
from core import app
from core.user.schema import user_schema


def get_access_token():
    with app.test_request_context():
        client = Client(user_schema)
        auth = client.execute(
            """
            mutation AuthUser($username: String, $password: String) {
                authUser(username: $username, password: $password) {
                    accessToken
                    refreshToken
                }
            }
        """,
            variable_values={
                "username": "automation_test",
                "password": "makeupstagegreatagain",
            },
        )
        accessToken = auth["data"]["authUser"]["accessToken"]
        return accessToken
