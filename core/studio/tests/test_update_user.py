from graphene.test import Client
from flask import request
from core import app
from core.studio.tests import get_access_token
from core.studio.schema import studio_schema
from time import time


def execute_update_email(newEmail):
    with app.test_request_context():
        client = Client(studio_schema)
        request.headers = {"X-Access-Token": get_access_token()}

        executed = client.execute(
            """
                mutation UpdateUser($id: ID!, $displayName: String, $firstName: String, $lastName: String, $email: String, $password: String, $active: Boolean, $role: Int, $uploadLimit: Int) {
                  updateUser(inbound: {id: $id, displayName: $displayName, firstName: $firstName, lastName: $lastName, email: $email, password: $password, active: $active, role: $role, uploadLimit: $uploadLimit}) {
                    user {
                      ...userFragment
                    }
                  }
                }

                fragment userFragment on AdminPlayer {
                  id
                  dbId
                  username
                  firstName
                  lastName
                  displayName
                  email
                  active
                  createdOn
                  role
                  uploadLimit
                  intro
                }
                """,
            variable_values={
                "id": "VXNlcjoxNjY=",
                "dbId": 166,
                "username": "teddy1",
                "firstName": "",
                "lastName": "",
                "displayName": "",
                "email": newEmail,
                "active": True,
                "createdOn": "2023-07-22T16:11:41.103693",
                "role": 4,
                "uploadLimit": 1048576,
                "intro": "",
            },
        )
        return executed


def test_update_email_existed():
    newEmail = "hongphat.js@gmail.com"
    executed = execute_update_email(newEmail)
    assert (
        executed["errors"][0]["message"]
        == "This email address already belongs to another user!"
    )


def test_update_email_success():
    timestamp = str(int(time()))
    newEmail = f"test.{timestamp}@gmail.com"
    executed = execute_update_email(newEmail)
    assert executed["data"]["updateUser"]["user"]["email"] == newEmail
