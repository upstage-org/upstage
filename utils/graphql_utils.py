# -*- coding: iso8859-15 -*-
import sys,os
from collections import namedtuple
import json
import pytz

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from graphql_relay.node.node import from_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from config.project_globals import app,DBSession
from user.user_api import current_user
from auth.auth_api import TNL,jwt_required

def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
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
        omitted = ('password',)
        for name, val in args.items():
            if name in omitted: continue
            col = getattr(model, name, None)
            if col:
              query = query.filter(col == val)
        return query


class CurrentUserField(SQLAlchemyConnectionField):

    def __init__(self, type, input_type, *args, **kwargs):
        #fields = {name: field.type() for name, field in input_type._meta.fields.items()}
        #kwargs.update(fields)
        self.result={}
        super().__init__(type, *args, **kwargs)

    @classmethod
    @jwt_required
    def get_query(cls, model, info, sort=None, **args):
        print("here 1")
        code,error,user,buildings,groups,timezone = current_user()
        if code != 200:
            abort(code,error)

        print("here 2")
        access_token = request.headers.get(app.config['JWT_HEADER_NAME'],None)
        #app.logger.info("access token:{0}".format(access_token))
    
        print("here 3")
        # If latest user session access token doesn't match, kick them out.
        user_session = DBSession.query(UserSession).filter(
            UserSession.user_id==user.id).order_by(
            UserSession.recorded_time.desc()).first()
  
        print("here 4")
        if not user_session:
            abort(403,'Bad user session (3)')

        print("here 5")
        if (user_session.access_token != access_token):
            TNL.add(access_token)
            # No. user session may be valid, from a newer login on a different device.
            #TNL.add(user_session.refresh_token)
            #TNL.add(user_session.access_token)
            abort(403,'Access token is invalid (4)')

        print("here 6")
        self.result = {
            'user_id':user.id,'role':user.role,
            'phone':user.phone,
            'first_name':user.first_name, 'last_name': user.last_name,
            'email':user.email,
            'timezone':timezone if timezone != pytz.UTC else None,
            'groups':[],
            'username':user.username,
            }
        return self.result
  
