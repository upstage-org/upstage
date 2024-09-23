from typing import List
from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from core.helpers.object import convert_keys_to_camel_case
from ariadne.asgi import GraphQL
from mails.helpers.mail import send
from studios.graphql.studio import type_defs
from studios.http.validation import BatchUserInput, ChangePasswordInput, UpdateUserInput
from studios.services.studio import StudioService
from users.entities.user import ADMIN, ROLES, SUPER_ADMIN, UserEntity


query = QueryType()
mutation = MutationType()


@query.field("whoami")
@authenticated()
def current_user(_, info):
    user = info.context["request"].state.current_user
    return convert_keys_to_camel_case({**user, "roleName": ROLES[int(user["role"])]})


@query.field("adminPlayers")
@authenticated()
def admin_players(_, __, **kwargs):
    return StudioService().admin_players(kwargs)


@mutation.field("batchUserCreation")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN])
def create_users(_, __, users: List[BatchUserInput]):
    print(users)
    return StudioService().create_users(users)


@mutation.field("updateUser")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN])
async def update_user(_, __, input: UpdateUserInput):
    return await StudioService().update_user(UpdateUserInput(**input))


@mutation.field("deleteUser")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN])
def delete_user(_, info, id: int):
    return StudioService().delete_user(
        id, UserEntity(**info.context["request"].state.current_user)
    )


@mutation.field("sendEmail")
@authenticated()
async def send_email(_, __, input):
    await send(
        input["recipients"].split(","),
        input["subject"],
        input["body"],
        input["bcc"].split(",") if input["bcc"] else [],
    )
    return {"success": True}


@mutation.field("changePassword")
@authenticated()
def change_password(_, __, input: ChangePasswordInput):
    return StudioService().change_password(ChangePasswordInput(**input))


@mutation.field("calcSizes")
def calc_sizes(_, __):
    return StudioService().calc_sizes()


@mutation.field("requestPermission")
@authenticated()
def request_permission(_, info, asset_id: int, note: str):
    return StudioService().request_permission(
        UserEntity(**info.context["request"].state.current_user), asset_id, note
    )


@mutation.field("confirmPermission")
@authenticated()
def confirm_permission(_, info, id: int, approved: bool):
    return StudioService().confirm_permission(
        UserEntity(**info.context["request"].state.current_user), id, approved
    )


@mutation.field("quickAssignMutation")
@authenticated()
def quick_assign_mutation(_, info, stage_id: int, asset_id: int):
    return StudioService().quick_assign_mutation(
        UserEntity(**info.context["request"].state.current_user), stage_id, asset_id
    )


schema = make_executable_schema(type_defs, query, mutation)
studio_graphql_app = GraphQL(schema, debug=True)
