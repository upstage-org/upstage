import wrapt

from config.project_globals import app,api
from user.models import (ATTENDEE,PARTICIPANT,
    ACCOUNT_ADMIN,SUPER_ADMIN)
from user.user_utils import current_user

'''
Roles are handled here, and are treated like static content. 
Groups will be handled in the data model, and are considered dynamic.
'''

# Ensure True/False is always returned.
# User can actually be in multiple roles.

@wrapt.decorator
def role_attendee(fn, instance, args, kwargs):
    code,error,user,x,y,t = current_user()
    if code != 200:
        abort(code,error)

    if (user.role & ATTENDEE) != 0:
        return fn(*args, **kwargs)
    app.logger.warning("Denied access to fn {0} for user {1}:{2}, user is not role {3}".format(
        str(fn),user.id,user.email,ROLES[RESIDENT]))
    
@wrapt.decorator
def role_participant(fn, instance, args, kwargs):
    code,error,user,x,y,t = current_user()
    if code != 200:
        abort(code,error)

    if (user.role & PARTICIPANT) != 0:
        return fn(*args, **kwargs)
    app.logger.warning("Denied access to fn {0} for user {1}:{2}, user is not role {3}".format(
        str(fn),user.id,user.email,ROLES[PROVIDER]))
    
@wrapt.decorator
def role_acct_admin(fn, instance, args, kwargs):
    code,error,user,x,y,t = current_user()
    if code != 200:
        abort(code,error)

    if (user.role & ACCOUNT_ADMIN) != 0:
        return fn(*args, **kwargs)
    app.logger.warning("Denied access to fn {0} for user {1}:{2}, user is not role {3}".format(
        str(fn),user.id,user.email,ROLES[ACCOUNT_ADMIN]))
    
@wrapt.decorator
def role_super_admin(fn, instance, args, kwargs):
    code,error,user,x,y,t = current_user()
    if code != 200:
        abort(code,error)

    if (user.role & SUPER_ADMIN) != 0:
        return fn(*args, **kwargs)
    app.logger.warning("Denied access to fn {0} for user {1}:{2}, user is not role {3}".format(
        str(fn),user.id,user.email,ROLES[SUPER_ADMIN]))
    

