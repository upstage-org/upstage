# -*- coding: iso8859-15 -*-
import os,sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from ariadne import (gql, ObjectType,QueryType,
    MutationType,make_executable_schema)
from ariadne.asgi import GraphQL
from dataclasses import dataclass,field
from fastapi import FastAPI,status,Body,Header,Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from typing import List,Annotated,Union,Optional

from upstage_config import project_config as config

from authn.data_tools import AdminDataInterface
from authn.jwt_tools import JWTInterface
from authn.login_tools import (LoginInterface,
    USER_VERIFICATION,PASSWORD_RESET)
from authz.permissions_tools import (PermissionsInterface,
    HARDCODED_DEFAULT_LINK)
from run.fastapi_exception_handlers import RequestExceptionHandling

def find_in_gql_header(info,variable):
    '''
    nginx limits HTTP headers to a maximum of 1k.
    '''
    b_variable = str.encode(variable)
    if info and 'request' in info.context and 'headers' in info.context['request'].scope:
        for header in info.context['request'].scope['headers']:
            if header[0] == b_variable:
               return header[1].decode('utf-8') 

app = FastAPI()
REH = RequestExceptionHandling(logger)

app.add_exception_handler(RequestValidationError, REH.request_validation_exception_handler)
app.add_exception_handler(HTTPException, REH.http_exception_handler)
app.add_exception_handler(Exception, REH.unhandled_exception_handler)

DEBUG=False
if config.ENV != 'Production':
    logger.warning("WARNING: ENV is NOT set to Production. Is this what you want?")
    from fastapi.middleware.cors import CORSMiddleware

    origins = [
        f"http://localhost:{config.FASTAPI_PORT}",
        f"http://127.0.0.1:{config.FASTAPI_PORT}",
        ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )
    DEBUG=True

# Create GraphQL type definitions
type_defs = gql("""
    scalar BigInt

    type LoginResponse {
        access_key: String
        refresh_key: String
        link: String
        error: String
    }

    type BoolResponse {
        response: Boolean
        error: String
    }

    type TempCodeResponse {
        temporary_code: String
        error: String
    }

    type UserResponse {
        local_login:String
        email:String
        description:String
        expires_timestamp_seconds:BigInt
    }

    type AllUsersResponse {
        users:[UserResponse]
        error: String
    }

    # Authn: permissions and groups handling below
    type PermissionResponse {
        namespace:String
        permission_value:BigInt
        label:String
    }

    type GroupResponse {
        namespace:String
        group_name:String
        permissions_bitmask:BigInt
        permissions_detail:[PermissionResponse]
        expires_timestamp_seconds:BigInt
    }

    input UserGroupRequest {
        namespace:String
        group_names:[String]
    }

    input UserGroupsRequest {
        user_groups_request:[UserGroupRequest]
    }

    type UserGroupResponse {
        namespace:String
        group_name:String
        permissions_bitmask:BigInt
        permissions_detail:[PermissionResponse]
        expires_timestamp_seconds:BigInt
    }

    type NamespaceResponse {
        link_url:String
        namespace:String
        group_names:[String]
    }

    type AllNamespacesResponse {
        namespaces:[NamespaceResponse]
        error: String
    }

    type AllGroupsResponse {
        active: [GroupResponse]
        expired: [GroupResponse]
        error: String
    }

    type AllPermissionsResponse {
        permissions: [PermissionResponse]
        error: String
    }

    type UserGroupsResponse {
        groups: [UserGroupResponse]
        error: String
    }

    type PermissionsCheckResponse {
        response: Boolean
        error: String
    }

    type Query {
        is_logged_in: Boolean
        logout: Boolean
        admin_permissions: Boolean
        get_all_users: AllUsersResponse
        get_all_groups: AllGroupsResponse
        get_all_permissions: AllPermissionsResponse
        get_all_namespaces: AllNamespacesResponse
        get_my_groups: UserGroupsResponse
        get_next_bitmask_value(namespace:String): Int
        do_i_have_these_permissions(local_login:String,namespace:String,group_name:String,bit_settings:BigInt): Boolean

    }
    type Mutation {
        login(local_login:String,password:String,namespace:String): LoginResponse
        refresh(refresh_key:String): LoginResponse
        new_or_existing_user(local_login:String,password:String,email:String,description:String,expires_timestamp_seconds:BigInt): BoolResponse
        verify_user(temporary_code:String): TempCodeResponse
        change_password(password1:String,password2:String,temporary_code:String): BoolResponse
        send_verification_email(local_login:String): BoolResponse
        forgot_password_verification_email(local_login:String): BoolResponse
        delete_user(local_login:String): BoolResponse
        add_change_group(namespace:String, group_name:String, permissions_bitmask:BigInt,expires_timestamp_seconds:BigInt,add:Boolean): BoolResponse
        delete_group(namespace:String, group_name:String): BoolResponse
        add_change_permission(namespace:String, permission:BigInt, label:String, add:Boolean): BoolResponse
        delete_permission(namespace:String, permission:BigInt): BoolResponse
        add_change_namespace(namespace:String, link_url:String): BoolResponse
        delete_namespace(namespace:String): BoolResponse
        set_user_groups(local_login:String,groups_list:[UserGroupsRequest]): BoolResponse
        get_user_groups(local_login:String): UserGroupsResponse
    }
""")

@dataclass
class LoginRequest:
    local_login: str
    password: str = None
    namespace: str = None
    error: str = None

@dataclass
class BoolResponse:
    response: bool = None
    error: str = None

@dataclass
class TempCodeResponse:
    temporary_code: str = None
    error: str = None

@dataclass
class LoginResponse:
    access_key: str = None
    refresh_key: str = None
    link: str = None
    error: str = None

@dataclass
class RefreshRequest:
    refresh_key: str

@dataclass
class UserResponse:
    local_login:str = None
    email:str = None
    description:str = None
    expires_timestamp_seconds:int = None

@dataclass
class AllUsersResponse:
    users: list[UserResponse] = None
    error: str = None

# Authn below
@dataclass
class PermissionResponse:
    namespace:str = None
    permission_value:int = None
    label:int = None

@dataclass
class GroupResponse:
    namespace:str = None
    group_name:str = None
    permissions_bitmask:int = None
    permissions_detail:list[PermissionResponse] = None
    expires_timestamp_seconds:int = None

@dataclass
class UserGroupResponse:
    namespace:str = None
    group_name:str = None
    permissions_bitmask:int = None
    permissions_detail:list[PermissionResponse] = None
    expires_timestamp_seconds:int = None

@dataclass
class NamespaceResponse:
    namespace:str = None
    link_url:str = None
    group_names:list[str] = None

@dataclass
class AllNamespacesResponse:
    namespaces:list[NamespaceResponse] = None
    error: str = None

@dataclass
class AllGroupsResponse:
    active: list[GroupResponse] = None
    expired: list[GroupResponse] = None
    error: str = None

@dataclass
class AllPermissionsResponse:
    permissions: list[PermissionResponse] = None
    error: str = None

@dataclass
class UserGroupRequest:
    namespace:str
    group_names:list[str]

@dataclass
class UserGroupsRequest:
    user_groups_request:list[UserGroupRequest]

@dataclass
class UserGroupsResponse:
    groups: list[UserGroupResponse] = None
    error: str = None

@dataclass
class PermissionsCheckResponse:
    response: bool = None
    error: str = None

query = QueryType()
mutation = MutationType()


''' 
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
User-level endpoints.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
''' 
@query.field("is_logged_in")
def resolve_is_logged_in(_,info,access_key=None):
    if not access_key:
        access_key = find_in_gql_header(info,'x-access-token')
    local_login = JWTInterface(logger).is_logged_in(access_key)
    '''
    Make sure user account wasn't deleted/expired.
    '''
    if local_login:
        return LoginInterface(logger).find_user(local_login)
    return False

@query.field("logout")
def resolve_logout(_, info,access_key=None):
    if not access_key:
        access_key = find_in_gql_header(info,'x-access-token')
    JWTInterface(logger).logout(access_key)
    return True

@query.field("admin_permissions")
def resolve_admin_permissions(_,info,access_key=None):
    if not access_key:
        access_key = find_in_gql_header(info,'x-access-token')
    local_login = JWTInterface(logger).is_logged_in(access_key)
    if (not local_login):
        return False
    return PermissionsInterface(logger).has_local_admin_permissions(local_login)

@mutation.field("login")
def resolve_login(_,info,local_login:str,password:str,namespace:str = None):
    if LoginInterface(logger).login(local_login,password):
        link = link_url = None
        pi = PermissionsInterface(logger)
        if not pi.has_local_admin_permissions(local_login):
            '''
            Try to find a sensible landing page for this user, even if they did not specify a namespace.
            If they belong to > 1 namespace, we send them to the default.
            '''
            if namespace:
                link_url = pi.verify_user_in_namespace(local_login)

            if not link_url:
                aun = pi.get_all_user_namespaces(local_login)
                if (len(aun) > 1) or (len(aun) <= 0):
                    link_url = HARDCODED_DEFAULT_LINK
                else:
                    link_url = aun[0]['link_url']

            if link_url:
                '''
                A non-admin user gets redirected after initial login. They only see the new refresh token. 
                They have to immeidately issue a refresh to get new tokens at that point. Make this timeout short
                for that reason.
                '''
                access_key, refresh_key = JWTInterface(logger).login(local_login,
                    custom_timeout_seconds=config.JWT_INITIAL_REDIRECT_REFRESH_TOKEN_TIMEOUT_SECONDS)
                link = f'{link_url}?refresh_token={refresh_key}&local_login={local_login}'
                if access_key and refresh_key:
                    lr = LoginResponse(None,None,link=link)
                    return lr
        else:
            '''
            User is an admin, they will get sent to the admin landing page.
            The admin tokens have a shorter timeout than the user tokens.
            '''
            access_key, refresh_key = JWTInterface(logger).login(local_login,admin_timeout_seconds=True)
            lr = LoginResponse(access_key=access_key,refresh_key=refresh_key,link=None)
            return lr
    return LoginResponse(error="Login did not succeed, or user is not in the specified namespace.")

@mutation.field("refresh")
def resolve_refresh(_, info, refresh_key:str):
    jwti = JWTInterface(logger)
    access_key,new_refresh_key,local_login = jwti.refresh(refresh_key)
    '''
    Make sure user account wasn't deleted/expired.
    '''
    if access_key and new_refresh_key:
        if LoginInterface(logger).find_user(local_login):
            lr = LoginResponse(access_key=access_key,refresh_key=new_refresh_key,link=None)
            return lr
        jwti.expire_by_force(access_key,refresh_key)
        jwti.expire_by_force(None,new_refresh_key)
    return LoginResponse(error="Refresh Failed")

'''
This is used for newly-registered users and users changing their password.
This was accessed through a ReST email link, and 
redirects to the change password page with a new emebdded code.
There's no email sent here.
'''
@mutation.field("verify_user")
def resolve_verify_user(_, info, temporary_code:str):
    li = LoginInterface(logger)
    local_login,reason = li.verify_temporary_code(temporary_code)
    if local_login:
        if reason == USER_VERIFICATION:
            temp_code = li.generate_temporary_code(
                local_login=local_login,reason=PASSWORD_RESET)
            if temp_code:
                logger.info(f"In resolve_verify_user, temp code for password reset is {temp_code}")
                '''
                This gets sent to a VueJS page, which prompts for the password1 and 2 values.
                '''
                #tcr = TempCodeResponse()
                #tcr.temporary_code = temp_code
                #return tcr
                return RedirectResponse(url=f'/change_password?temporary_code={temp_code}',
                    status_code=303)
    return TempCodeResponse(error="Verify user failed.")

'''
This is called by the above generated change_password email link.
'''
@mutation.field("change_password")
def resolve_change_password(_, info, password1:str, password2:str, temporary_code:str):
    li = LoginInterface(logger)
    local_login,reason = li.verify_temporary_code(temporary_code)
    if local_login:
        if reason == PASSWORD_RESET:
            response = li.change_password(local_login,password1,password2)
            if response==True:
                br = BoolResponse(response)
                return br
    return BoolResponse(error="Change Password failed.")

'''
Any time a regular non-admin user wants to change their password, they have to call this.
'''
@mutation.field("forgot_password_verification_email")
def resolve_forgot_password_verification_email(_, info, local_login:str):
    response = None
    li = LoginInterface(logger)
    if li.find_user(local_login):
        temp_code = li.generate_temporary_code(
            local_login=local_login,reason=USER_VERIFICATION)
        if temp_code:
            link=f'{config.VERIFY_USER_URL}?temporary_code={temp_code}'
            response = li.send_verification_email(local_login,link)
            if response == None:
                br = BoolResponse(True)
                return br
    else:
        response = "No temporary code generated"
    return BoolResponse(error=response)

'''
Authz non-admin endpoints to find one's own groups and permissions.
'''
@query.field("get_my_groups")
def resolve_get_my_groups(_,info):
    access_key = find_in_gql_header(info,'x-access-token')
    local_login = JWTInterface(logger).is_logged_in(access_key)
    if not local_login:
        return UserGroupsResponse(error='Please log in')

    outbound = []
    pi = PermissionsInterface(logger)
    result = pi.find_groups_for_user(local_login)
    for r in result:
        pr = [PermissionResponse(
            namespace=p['namespace'],
            permission_value=p['permission_value'],
            label=p['label'],
            ) for p in r['permissions_detail']]
        outbound.append(
            UserGroupResponse(
                namespace=r['namespace'],
                group_name=r['group_name'],
                permissions_bitmask=r['permissions_bitmask'],
                expires_timestamp_seconds=r['expires_timestamp_seconds'],
                permissions_detail=pr,
                )
            )
    if outbound:
        return UserGroupsResponse(groups=outbound)
    return UserGroupsResponse(error='No results found')

@query.field("do_i_have_these_permissions")
def resolve_do_i_have_these_permissions(_,info,local_login,namespace,
    group_name,bit_settings=None):

    access_key = find_in_gql_header(info,'x-access-token')
    local_login = JWTInterface(logger).is_logged_in(access_key)
    if not local_login:
        return BoolResponse(error='PLease log in.')

    pi = PermissionsInterface(logger)
    return pi.does_user_have_this_permission(local_login,namespace,
        group_name,bit_settings)

''' 
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Admin-only endpoints.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
@mutation.field("new_or_existing_user")
def resolve_new_or_existing_user(_, info, local_login=None,password=None,email=None,description=None,
    expires_timestamp_seconds=None):
    if resolve_admin_permissions(_,info):
        result=None
        li = LoginInterface(logger)
        response,is_new=li.new_or_existing_user(local_login,password,email,description,
            expires_timestamp_seconds)
        if response == True:
            if is_new:
                temp_code = li.generate_temporary_code(
                    local_login=local_login,reason=USER_VERIFICATION)
                link=f'{config.VERIFY_USER_URL}?temporary_code={temp_code}'
                result = li.send_verification_email(local_login=local_login,link=link)
                if result==None:
                    br = BoolResponse(True)
                    return br
            br = BoolResponse(True)
            return br
    return BoolResponse(error="Add/change user failed.")

@mutation.field("send_verification_email")
def resolve_send_verification_email(_, info, local_login:str):
    '''
    This is ent upon new user creation.
    It will be resent to force a user to change their password also.
    User gets a verification link, and clicking on it generates a change_password 
    action.
    '''
    response = None
    if resolve_admin_permissions(_,info):
       li = LoginInterface(logger)
       temp_code = li.generate_temporary_code(
           local_login=local_login,reason=USER_VERIFICATION)
       if temp_code:
           link=f'{config.VERIFY_USER_URL}?temporary_code={temp_code}'
           response = li.send_verification_email(local_login,link)
           if response == None:
               br = BoolResponse(True)
               return br
       else:
           response = "No temporary code generated"
    return BoolResponse(error=response)

@query.field("get_all_users")
def resolve_get_all_users(_, info):
    outbound = []
    if resolve_admin_permissions(_,info):
        for x in AdminDataInterface(logger).get_all_users():
            aur = UserResponse(
                local_login = x['local_login'],
                email = x['email'],
                description = x['description'],
                expires_timestamp_seconds = x['expires_timestamp_seconds'],
                )
            outbound.append(aur)
    if not outbound:
        return AllUsersResponse(error='No results found')
    return AllUsersResponse(users=outbound)

@mutation.field("delete_user")
def resolve_delete_user(_, info, local_login:str):
    response = None
    if resolve_admin_permissions(_,info):
        LoginInterface(logger).delete_login(local_login)
        PermissionsInterface(logger).cleanout_deleted_user(local_login)
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

'''
Admin-level Authz endpoints: groups, permissions, and assignment of groups to users.
'''
@query.field("get_all_permissions")
def resolve_get_all_permisions(_,info):
    outbound = []
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        result = pi.get_all_permission_labels()
        for r in result:
            outbound.append(
                PermissionResponse(
                    namespace=r['namespace'],
                    permission_value=r['permission_value'],
                    label=r['label'],
                    )
                )
        return AllPermissionsResponse(permissions=outbound)
    return AllPermissionsResponse(error='No results found')

@query.field("get_all_namespaces")
def resolve_get_all_namespaces(_,info):
    outbound = []
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        result = pi.get_all_namespaces()
        for r in result:
           outbound.append(NamespaceResponse(
               namespace = r['namespace'],
               link_url = r['link_url'],
               group_names = r['group_names'],
               ))
        return AllNamespacesResponse(namespaces=outbound)
    return AllNamespacesResponse(error='none found')

@query.field("get_all_groups")
def resolve_get_all_groups(_,info):
    outbound = []
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        result = pi.get_all_available_groups()
        o1 = []
        o2 = []
        for r in result['active']:
            pr = [PermissionResponse(
                namespace=p['namespace'],
                permission_value=p['permission_value'],
                label=p['label'],
                ) for p in r['permissions_detail']]
            o1.append(
                GroupResponse(
                    namespace=r['namespace'],
                    group_name=r['group_name'],
                    permissions_bitmask=r['permissions_bitmask'],
                    expires_timestamp_seconds=r['expires_timestamp_seconds'],
                    permissions_detail=pr,
                    )
                )
        for r in result['expired']:
            pr = [PermissionResponse(
                namespace=p['namespace'],
                permission_value=p['permission_value'],
                label=p['label'],
                ) for p in r['permissions_detail']]
            o2.append(
                GroupResponse(
                    namespace=r['namespace'],
                    group_name=r['group_name'],
                    permissions_bitmask=r['permissions_bitmask'],
                    expires_timestamp_seconds=r['expires_timestamp_seconds'],
                    permissions_detail=pr,
                    )
                )
        return AllGroupsResponse(active=o1,expired=o2)
    return AllGroupsResponse(error='No results found')

@mutation.field("add_change_group")
def resolve_add_change_group(_,info,namespace, group_name, permissions_bitmask,
    expires_timestamp_seconds=None,add=True):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.add_change_available_group(namespace,group_name,
            permissions_bitmask,expires_timestamp_seconds,add)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("delete_group")
def resolve_delete_group(_,info,namespace,group_name):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.delete_available_group(namespace,group_name)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("add_change_permission")
def resolve_add_change_permission(_,info, namespace, permission, label, add=True):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.add_change_permission_label(namespace,permission,
            label,add)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@query.field("get_next_bitmask_value")
def resolve_get_next_bitmask_value(_,info,namespace):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        return pi.calc_next_permission_bitmask(namespace)

@mutation.field("delete_permission")
def resolve_delete_permission(_,info,namespace, permission:int):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.delete_permission_label(namespace,permission)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("add_change_namespace")
def resolve_add_change_namespace(_,info,namespace:str, link_url:str = None):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.add_change_namespace(namespace,link_url)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("delete_namespace")
def resolve_delete_namespace(_,info,namespace:str):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.delete_namespace(namespace)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("set_user_groups")
def resolve_set_user_groups(_,info,local_login,groups_list:list[UserGroupsRequest]):
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        error_msg = pi.save_groups_for_user(local_login,groups_list)
        if error_msg:
            br = BoolResponse(error=error_msg)
            return br
        br = BoolResponse(True)
        return br
    br = BoolResponse(False)
    return br

@mutation.field("get_user_groups")
def resolve_get_user_groups(_,info,local_login):
    outbound = []
    if resolve_admin_permissions(_,info):
        pi = PermissionsInterface(logger)
        result = pi.find_groups_for_user(local_login)
        logger.warning(result)
        for r in result:
            pr = [PermissionResponse(
                namespace=p['namespace'],
                permission_value=p['permission_value'],
                label=p['label'],
                ) for p in r['permissions_detail']]
            outbound.append(
                UserGroupResponse(
                    namespace=r['namespace'],
                    group_name=r['group_name'],
                    permissions_bitmask=r['permissions_bitmask'],
                    expires_timestamp_seconds=r['expires_timestamp_seconds'],
                    permissions_detail=pr,
                    )
                )
        return UserGroupsResponse(groups=outbound)
    return UserGroupsResponse(error='No results found')

'''
GQL schema parsing and go-live.
'''
schema = make_executable_schema(type_defs, query, mutation)

'''
Attach GraphQL endpoint to FastAPI app
'''
app.mount("/graphql/", GraphQL(schema,debug=DEBUG))

'''
FastAPI ReSTful endpoints: call underlying graphql methods, return same data.
'''
# This link is embedded in emails for first-time user email verification.
@app.get("/verify_user/")
async def rest_get_verify_user(temporary_code: str):
    return resolve_verify_user(None,None,temporary_code)

@app.post("/login/")
async def rest_post_login(login_request: LoginRequest):
    '''
    Defining the LoginRequest for the ReST call causes the values to be
    retrieved from the post body.
    '''
    #return resolve_login(None,None,username,password) or JSONResponse(content=None,status_code=404)
    return resolve_login(None,None,login_request.local_login,
        login_request.password,login_request.namespace)

@app.post("/refresh/")
async def rest_post_refresh(refresh_request: RefreshRequest):
    print(refresh_request.refresh_key)
    return resolve_refresh(None,None,refresh_request.refresh_key)

@app.get("/is_logged_in/")
async def rest_get_is_logged_in(request:Request):
    access_key = request.headers.get('x-access-token')
    return resolve_is_logged_in(None,None,access_key)

@app.get("/logout/")
async def rest_get_logout(request:Request):
    access_key = request.headers.get('x-access-token')
    return resolve_logout(None,None,access_key)

# Run the FastAPI app locally, not via gunicorn. Only for testing.
if __name__ == "__main__":
    import uvicorn
    import uvicorn.config

    @app.on_event('startup')
    async def local_startup_event(): 
        # loguru Logging Options
        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<green>{time}</green> <level>{message}</level>",
        )
        logger.add("/var/log/gunicorn/access.log", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True)
        logger.add("/var/log/gunicorn/error.log", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True)
        logger.add("/var/log/gunicorn/log.json", rotation="500 MB", enqueue=True, backtrace=True, diagnose=True, serialize=True)
        logger.level('DEBUG')


    '''
    Production run should be invoked by gunicorn or some other ASGI spawner.
    '''
    uvicorn.run(app, host=config.FASTAPI_HOST, port=config.FASTAPI_PORT)

    '''
    When testing a single instance directly, run:
    uvicorn fastapi_jwt:app --reload --host 0.0.0.0 --port 8005 &
    '''
