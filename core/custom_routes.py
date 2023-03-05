# -*- coding: iso8859-15 -*-
import os, sys
import json

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)
import time, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, g
from flask import Response, jsonify, make_response

from werkzeug.routing import BaseConverter


def load_regex_converter(app):
    class RegexConverter(BaseConverter):
        def __init__(self, url_map, *items):
            super(RegexConverter, self).__init__(url_map)
            self.regex = items[0]

    app.url_map.converters["regex"] = RegexConverter
