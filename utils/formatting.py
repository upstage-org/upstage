import sys,os
import string
import unicodedata

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


def to_dict(i, ignore_relationships=False):
    if not i:
       return {}
    d={}
    for (x, y) in i.__dict__.items():
        if x != '_sa_instance_state':
            d[x]=y
    return d

