from ariadne import MutationType, make_executable_schema
from licenses.http.graphql import type_defs
from ariadne.asgi import GraphQL

from licenses.http.validatiion import LicenseInput
from licenses.services.license import LicenseService


mutation = MutationType()


mutation.field("createLicense")


def create_license(_, __, input):
    return LicenseService().create_license(LicenseInput(**input))


schema = make_executable_schema(type_defs, mutation)
license_graphql_app = GraphQL(schema, debug=True)
