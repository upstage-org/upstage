# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from config.project_globals import (DBSession,Base,metadata,engine,get_scoped_session,
    app,api)
from config.settings import VERSION
from auth.auth_api import jwt_required
from user.models import User as UserModel
from flask_graphql import GraphQLView
from auth.fernet_crypto import encrypt,decrypt

class UserAttribute:
    username = graphene.String(description="Username.")
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
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class CreateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to create a user."""
    pass


class CreateUser(graphene.Mutation):
    """Mutation to create a user."""
    user = graphene.Field(lambda: User, description="User created by this mutation.")

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        user = UserModel(**data)
        # Add validation for non-empty passwords, etc.
        user.password = encrypt(user.password)
        db_session.add(user)
        db_session.commit()
        db_session.close()

        return CreateUser(user=user)


class UpdateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update a user."""
    id = graphene.ID(required=True, description="Global Id of the user.")


class UpdateUser(graphene.Mutation):
    """Update a user."""
    user = graphene.Field(lambda: User, description="User updated by this mutation.")

    class Arguments:
        input = UpdateUserInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        local_db_session = get_scoped_session()

        local_db_session.query(UserModel)\
            .filter_by(id=data['id'])\
            .update(data, synchronize_session=False)
        db_session.commit()
        db_session.close()
        user = DBSession(User).filter_by(id=data['id']).first()

        return UpdateUser(user=user)


class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    userList = SQLAlchemyConnectionField(User.connection)

user_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/user_graphql/', view_func=GraphQLView.as_view("user_graphql", schema=user_schema,
    graphiql=True
    ))

