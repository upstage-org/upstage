# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'../..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import Flask, Blueprint, jsonify, request, url_for, send_file
from config.project_globals import app,DBSession,ScopedSession
from flask_graphql import GraphQLView
from performance.schema import performance_schema

# Graphql init
app.add_url_rule('/performance_graphql/', view_func=GraphQLView.as_view(
    'performance_graphql',
    schema=performance_schema,
    graphiql=True,
))

# Optional, for adding batch query support (used in Apollo-Client)
app.add_url_rule('/performance_graphql/batch/', view_func=GraphQLView.as_view(
    'performance_graphql',
    schema=performance_schema,
    batch=True
))


'$SYS/broker/clients/connected'
