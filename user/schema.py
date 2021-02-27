# -*- coding: iso8859-15 -*-
import sys,os
import json

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from config.project_globals import (DBSession,Base,metadata,engine,get_scoped_session,
    app,api,ScopedSession)
from config.settings import VERSION
from auth.auth_api import jwt_required
from user.models import User as UserModel
from flask_graphql import GraphQLView
from auth.fernet_crypto import encrypt,decrypt
from utils import graphql_utils
from auth.auth_mutation import AuthMutation,RefreshMutation
from flask_jwt_extended import jwt_required,get_jwt_identity

class UserAttribute:
    username = graphene.String(description="Username")
    password = graphene.String(description="Password")
    email = graphene.String(description="Email Address")
    bin_name = graphene.String(description="bin_name")
    role = graphene.Int(description="User Role")
    first_name = graphene.String(description="First Name")
    last_name = graphene.String(description="Last Name")
    display_name = graphene.String(description="Display Name")
    apartment = graphene.String(description="Apartment")
    phone = graphene.String(description="Phone")
    active =  graphene.Boolean(description="Active record or not")
    ok_to_sms = graphene.Boolean(description="Okay to sms?")
    validated_via_portal = graphene.Boolean(description="Validated")
    agreed_to_terms = graphene.Boolean(description="Agreed to terms")
    accept_rent_payment = graphene.Boolean(description="Accept rent payment")
    firebase_pushnot_id = graphene.String(description="firebase_pushnot_id")

class User(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    class Meta:
        model = UserModel
        model.db_id = model.id
        interfaces = (relay.Node,)

class CreateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to create a user."""
    pass

class CreateUser(graphene.Mutation):
    """Mutation to create a user."""
    user = graphene.Field(lambda: User, description="User created by this mutation.")

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)

        user = UserModel(**data)
        # Add validation for non-empty passwords, etc.
        user.password = encrypt(user.password)
        local_db_session = get_scoped_session()
        local_db_session.add(user)
        local_db_session.flush()
        user_id = user.id
        local_db_session.commit()

        user = DBSession.query(UserModel).filter(UserModel.id==user_id).first()
        return CreateUser(user=user)

class UpdateUserInput(graphene.InputObjectType,UserAttribute,):
    """Arguments to update a user."""
    id = graphene.ID(required=True, description="Global Id of the user.")

class UpdateUser(graphene.Mutation):
    """Update a user."""
    user = graphene.Field(lambda: User, description="User updated by this mutation.")

    class Arguments:
        input = UpdateUserInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        local_db_session = get_scoped_session()

        user = local_db_session.query(UserModel)\
            .filter(UserModel.id==data['id']).first()
        if ('password' in data):
            del data['password'] # Password should not be updated directly using this mutation, since it require an old password to change
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        local_db_session.commit()
        user = DBSession.query(UserModel).filter(UserModel.id==data['id']).first()

        return UpdateUser(user=user)

class OneUserInput(graphene.InputObjectType):
    username = graphene.String(required=False)
    db_id = graphene.Int(required=False)
    email = graphene.String(required=False)

class ChangePasswordInput(graphene.InputObjectType,UserAttribute,):
    """Arguments to update a user."""
    id = graphene.ID(required=True, description="Global Id of the user.")
    oldPassword = graphene.String(required=True)
    newPassword = graphene.String(required=True)

class ChangePassword(graphene.Mutation):
    success = graphene.Boolean(description="Password changed successful or not")

    class Arguments:
        input = ChangePasswordInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        local_db_session = get_scoped_session()
        user = local_db_session.query(UserModel).filter(UserModel.id==data['id']).first()
        if decrypt(user.password) != data['oldPassword']:
            raise Exception('Old password incorrect')
        else:
            user.password = encrypt(data['newPassword'])
        local_db_session.commit()
        return ChangePassword(success=True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    authUser = AuthMutation.Field()
    refreshUser = RefreshMutation.Field()
    changePassword = ChangePassword.Field()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    userList = SQLAlchemyConnectionField(User.connection)
    oneUser = graphql_utils.FilteredConnectionField(User, OneUserInput)
    currentUser = graphene.Field(User)

    @jwt_required()
    def resolve_currentUser(self, info):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            raise Exception("Your session expired. Please log in again.")
        query = User.get_query(info)
        user = query.get(current_user_id)
        return user

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
user_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/user_graphql/', view_func=GraphQLView.as_view("user_graphql", schema=user_schema,
    graphiql=True
))

