from graphene.test import Client
from core import app
from .schema import user_schema


def test_update_existed_email(snapshot):
    with app.app_context():
        client = Client(user_schema)
        snapshot.assert_match(
            client.execute(
                """
            {
                userList {
                    edges {
                    node {
                        id
                        username
                    }
                    }
                }
            }
        """
            )
        )
