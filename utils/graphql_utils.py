# -*- coding: iso8859-15 -*-
import sys,os

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


from graphql_relay.node.node import from_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary


# Enables querying based on specific field value pairs.
class FilteredConnectionField(SQLAlchemyConnectionField):

  def __init__(self, type, input_type, *args, **kwargs):
    fields = {name: field.type() for name, field in input_type._meta.fields.items()}
    import pprint
    pprint.pprint(fields)
    kwargs.update(fields)
    super().__init__(type, *args, **kwargs)

  @classmethod
  def get_query(cls, model, info, sort=None, **args):
      query = super().get_query(model, info, sort=sort, **args)
      #omitted = ('first', 'last', 'hasPreviousPage', 'hasNextPage', 'startCursor', 'endCursor')
      omitted = ()
      import pprint
      pprint.pprint(args)
      for name, val in args.items():
          if name in omitted: continue
          col = getattr(model, name, None)
          if col:
            query = query.filter(col == val)
      return query


