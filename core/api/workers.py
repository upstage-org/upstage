# -*- coding: iso8859-15 -*-
import os,sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from typing import Any, Dict
from uvicorn.workers import UvicornWorker as BaseUvicornWorker

class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS: Dict[str, Any] = {"loop": "auto", "http": "auto", "lifespan": "off"}

