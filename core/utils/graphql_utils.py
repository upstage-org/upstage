# -*- coding: iso8859-15 -*-
import sys, os
from collections import namedtuple
import json
import pytz

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from graphql_relay.node.node import from_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene

from core.project_globals import app, DBSession
from core.user.user_utils import current_user
from core.auth.auth_api import TNL, jwt_required


def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        if key[-2:] == "id":
            input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary


def _json_object_hook(d):
    return namedtuple("X", d.keys())(*d.values())


def json2obj(data):
    """Convert JSON to an object Graphene can handle"""
    return json.loads(data, object_hook=_json_object_hook)


# Enables querying based on specific field value pairs.
class FilteredConnectionField(SQLAlchemyConnectionField):
    def __init__(self, type, input_type, *args, **kwargs):
        fields = {name: field.type() for name, field in input_type._meta.fields.items()}
        kwargs.update(fields)
        super().__init__(type, *args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super().get_query(model, info, sort=sort, **args)
        omitted = ("password",)
        for name, val in args.items():
            if name in omitted:
                continue
            col = getattr(model, name, None)
            if col:
                query = query.filter(col == val)
        return query


class CountableConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return self.length


"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In case we want to pass errors directly to the front end...
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CustomClientIDMutationMeta(ClientIDMutationMeta):
    ''' We have to subclass the metaclass of ClientIDMutation and inject the errors field.
        we do this because ClientIDMutation subclasses do not inherit the fields on it.
    '''
    def __new__(mcs, name, bases, attrs):
        attrs['errors'] = String()
        return super().__new__(mcs, name, bases, attrs)

class CustomClientIDMutation(ClientIDMutation, metaclass=CustomClientIDMutationMeta):
    ''' Custom ClientIDMutation that has a errors  @fields.'''
    @classmethod
    def mutate(cls, root, args, context, info):
        try:
            return super().mutate(root, args, context, info)

        except MutationException as e:
            return cls(errors=str(e))

class MutationException(Exception):
    '''A Mutation Exception is an exception that is raised
       when an error message needs to be passed back to the frontend client
       our mutation base class will catch it and return it appropriately
    '''
    pass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
