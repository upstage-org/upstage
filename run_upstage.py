#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
import os
import sys

projdir = os.path.abspath(os.path.dirname(__file__))
if projdir not in sys.path:
    sys.path.append(projdir)

from dispatcher.main import application

if __name__ == "__main__":
    application.run()
