# -*- coding: iso8859-15 -*-
import os,sys
import json
import warnings
from decimal import Decimal
import logging

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import datetime
from flask_cors import CORS
from flask import Flask, redirect, g, got_request_exception, abort, render_template
from flask import Response, jsonify, make_response, request
from flask_caching import Cache as URLCache
from flask.json import JSONEncoder
#from flask.exthook import ExtDeprecationWarning
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Integer, Column, text

from config.settings import (ENV_TYPE,
    HOSTNAME,SQLALCHEMY_POOL_SIZE,
    SECRET_KEY,MAX_SESSION_SECONDS,DEBUG,FLASK_HOST,FLASK_PORT)

from config.crash_logger import log_handler, crash_mailer
from config.custom_routes import load_regex_converter
from config.settings import (SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,JWT_ACCESS_TOKEN_MINUTES,
    JWT_REFRESH_TOKEN_DAYS)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o,datetime.date):
            return o.isoformat()
        if isinstance(o, ObjectId) or isinstance(o,Decimal):
            return str(o)
        return JSONEncoder.default(self, o)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DB session setup
# Both global and local sessions are used. Local sessions are read-write.
engine = create_engine(SQLALCHEMY_DATABASE_URI,
    pool_size=SQLALCHEMY_POOL_SIZE, isolation_level="AUTOCOMMIT")

DBSession = scoped_session(sessionmaker(autocommit=True,autoflush=True,bind=engine))

Base = declarative_base()
metadata = Base.metadata
    
class ScopedSession(object):
    '''
    Use this for local session scope.
    Usage: 
        with ScopedSession as local_db_session:
           ...
           local_db_session.add(some db obj)
           local_db_session.flush() if you need the ID of your new obj right away
           or:
           some_obj = local_db_session.query(some db model).filter(...
           some_obj.field = some_new_value

    Session will be committed and closed when you fall out of scope.
    Rollback handling can be handled by you, or default to what is "expected".
    '''
    def __init__(self,rollback_upon_failure=True):
        self.session = scoped_session(sessionmaker(autocommit=True,autoflush=True,bind=engine))
        self.rollback_upon_failure = rollback_upon_failure

    def __enter__(self):
        self.session.begin()
        return self.session

    def __exit__(self):
        try:
            self.session.commit()
        except Exception as e:
            if self.rollback_upon_failure:
                self.session.rollback()
                logging.error(f"Failed to commit db session, rolled back: {e}")
            else:
                logging.error(f"Failed to commit db session, not rolled back, as per your request: {e}")
        finally:
            self.session.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initialize_microservice(app):
    # BYO app
    #app = Flask(__name__,static_url_path=None, 
    #    static_folder='/tmp')

    # RestX init
    api = Api(app,ui=False)

    app.secret_key = SECRET_KEY

    app.config.from_object('config.settings')
    app.url_map.strict_slashes=True

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=JWT_ACCESS_TOKEN_MINUTES)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=JWT_REFRESH_TOKEN_DAYS)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_HEADER_NAME'] = 'X-Access-Token'
    app.config['JWT_HEADER_TYPE'] = ''
    
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # This is only in effect when you call jsonify()
    app.json_encoder = CustomJSONEncoder
    
    db = SQLAlchemy(app)
    db.init_app(app)
    
    load_regex_converter(app)
    
    # Be sure to properly set your ENV_TYPE in config/settings/*.py
    print("Your environment type is: {0}".format(ENV_TYPE))

    '''
    Register crash handler and strict CORS rukes for production env.
    Only register crash handler for dev environments which run daemonized, like production.
    CORS is "off" for all other envirnments.
    '''

    if ENV_TYPE == "Production":
        app.debug = False
        crash_mailer(app,ENV_TYPE,HOSTNAME)
        log_handler(app)
        talisman = Talisman(app)
        print("Registering Crash Mailer")

    elif 'DEV' in ENV_TYPE:
        # Running crash reporting in dev when DEBUG is off, but not on individual machines.
        if DEBUG == False:
            print("Registering Crash Mailer")
            crash_mailer(app,ENV_TYPE,HOSTNAME)
        log_handler(app)
        CORS(app, resources={r"*": {"origins": "*"}})
    else:
        if DEBUG == False:
            app.debug = False
        else:
            app.debug = True
        CORS(app, resources={r"*": {"origins": "*"}})

        def add_cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            if request.method == 'OPTIONS':
                response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
                headers = request.headers.get('Access-Control-Request-Headers')
                if headers:
                    response.headers['Access-Control-Allow-Headers'] = headers
            return response

        app.after_request(add_cors_headers)
        log_handler(app)

    @app.errorhandler(500)
    def do500(e):
        return render_template("global_templates/500.html"), 500

    @app.errorhandler(404)
    def do404(e):
        return render_template("global_templates/404.html"), 404

    @app.errorhandler(403)
    def do403(e):
        return render_template("global_templates/403.html"), 403

    return db
