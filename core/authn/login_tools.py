# -*- coding: iso8859-15 -*-
import os,sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import arrow
import uuid

from scheduler_config import project_config as config
from authn.argon2_tools import new_hash,verify_hash
from mongo.mongo_connection import connect_to_mongo
from generic.send_emails import sendgrid_send_email

USER_VERIFICATION="User Verification (New and Existing)"
PASSWORD_RESET="Password Reset"

global mongo_connection
global mongo_db

mongo_connection,mongo_db = connect_to_mongo(
    db_name=config.MONGODB_DBNAME,
    connected_conn=None,
    connected_db=None,
    connect_string=config.MONGODB_CONNECT_STRING)

login_collection = mongo_db[config.MONGODB_LOGIN_COLLECTION_NAME]
temp_code_collection = mongo_db[config.MONGODB_TEMP_CODE_COLLECTION_NAME]

'''
This is maintained in jwt_tools.py, only here for user expiry.
'''
jwt_collection = mongo_db[config.MONGODB_JWT_TOKEN_COLLECTION_NAME]

'''
Clear and recreate indexes, in case of code changes.
'''
for dbindex in login_collection.list_indexes():
    if dbindex['name'] != '_id_':
        try:
            login_collection.drop_index(dbindex['name'])
        except:
            pass
for dbindex in temp_code_collection.list_indexes():
    if dbindex['name'] != '_id_':
        try:
            temp_code_collection.drop_index(dbindex['name'])
        except:
            pass
login_collection.create_index('local_login',unique=True)
login_collection.create_index('email',unique=True)
temp_code_collection.create_index('temp_code',unique=True,expireAfterSeconds=config.TEMP_CODE_TIMEOUT_SECONDS)

class InvalidExpiry(Exception):
    pass

class LoginInterface:
    '''
    All passwords will be hashed using the argon2id algorithm and
    stored here. This password cannot be unhashed. The user has to use
    the forgot password flow if their password isn't working.
    '''
    def __init__(self,logger):
        self.logger = logger

    def _save_credentials(self,local_login=None,password=None,email=None,
        description=None,expires_timestamp_seconds=None):

        '''
        Returns two bool parameters: result and is_new_user
        '''
        global mongo_connection
        global mongo_db

        mongo_connection,mongo_db = connect_to_mongo(
            db_name=config.MONGODB_DBNAME,
            connected_conn=mongo_connection,
            connected_db=mongo_db,
            connect_string=config.MONGODB_CONNECT_STRING)

        if expires_timestamp_seconds and (expires_timestamp_seconds <= 0):
            self.logger.exception(f"Invalid expiry timestamp passed to save_credentials: {expires_timestamp_seconds}, rejecting.")
            return False,False

        existing = self._find_credentials(local_login=local_login)
        use_local_login = local_login if (local_login not in ("",None)) else (existing['local_login'] if existing)
        use_password = new_hash(self.logger,password) if (password not in ("",None)) else (existing['password'] if existing else 'no password')
        use_email = email if (email not in ("",None)) else (existing['email'] if existing else None)
        use_description = description
        use_expires_timestamp_seconds = int(expires_timestamp_seconds) if expires_timestamp_seconds else None

        '''
        Passwords are hashed (above) using the argon2id algorithm.
        They cannot be unhashed.
        '''
        match_keys = {'local_login':use_local_login}

        try:
            login_collection.replace_one(
                match_keys,
                {'local_login':use_local_login,'password':use_password,'email':use_email,
                'description':use_description,
                'expires_timestamp_seconds':use_expires_timestamp_seconds},upsert=True)
        except:
            self.logger.exception("Failed to add/change user info:")
            return False,False

        if existing:
            '''
            2nd False = not new user
            '''
            return True,False
        return True,True

    def _find_credentials(self,local_login=None):
        global mongo_connection
        global mongo_db

        mongo_connection,mongo_db = connect_to_mongo(
            db_name=config.MONGODB_DBNAME,
            connected_conn=mongo_connection,
            connected_db=mongo_db,
            connect_string=config.MONGODB_CONNECT_STRING)

        '''
        Find unexpired credentials.
        '''
        result = login_collection.find_one({'local_login':local_login,
            '$or':[{'expires_timestamp_seconds':{'$gt':arrow.utcnow().timestamp()}},{'expires_timestamp_seconds':{'$eq':None}}]})
        if not result:
            self.logger.error(f"Credentials don't exist for local_login {local_login}")
            return
        return result


    def _expire_credentials(self,local_login,delete=False):
        global mongo_connection
        global mongo_db

        mongo_connection,mongo_db = connect_to_mongo(
            db_name=config.MONGODB_DBNAME,
            connected_conn=mongo_connection,
            connected_db=mongo_db,
            connect_string=config.MONGODB_CONNECT_STRING)

        if delete:
            login_collection.delete_one({'local_login':local_login})
        else:
            login_collection.replace_one(
                {'local_login':local_login},
                {'expires':arrow.utcnow().timestamp()},upsert=True)
        '''
        Delete many should not be necessary, but it's a precaution.
        '''
        temp_code_collection.delete_many({'local_login':local_login})
        jwt_collection.delete_many({'local_login':local_login})

    def _gen_temp_code(self,local_login=None,reason=USER_VERIFICATION):
        if (local_login in ('',None))
            self.logger.exception("Both local_login is not set. Rejecting.")
            return

        global mongo_connection
        global mongo_db

        mongo_connection,mongo_db = connect_to_mongo(
            db_name=config.MONGODB_DBNAME,
            connected_conn=mongo_connection,
            connected_db=mongo_db,
            connect_string=config.MONGODB_CONNECT_STRING)

        if reason == PASSWORD_RESET:
            obj = self._find_credentials(local_login=local_login)
            if not obj:
                self.logger.error(f"Can't generate code for change password for nonexistent or expired user: local_login {local_login}")
                return

            local_login = obj['local_login']

        if reason != PASSWORD_RESET:
            '''
            Delete all previous codes for this user if the reason is not password reset.
            For password resets, we let it expire naturally so they can try a couple of times
            in case they get it wrong.
            '''
            temp_code_collection.delete_many({'local_login':local_login})

        new_code = str(uuid.uuid4())
        temp_code_collection.insert_one({'local_login':local_login,
            'temp_code':new_code,'reason':reason})

        return new_code

    def _find_temp_code(self,temp_code):
        global mongo_connection
        global mongo_db

        mongo_connection,mongo_db = connect_to_mongo(
            db_name=config.MONGODB_DBNAME,
            connected_conn=mongo_connection,
            connected_db=mongo_db,
            connect_string=config.MONGODB_CONNECT_STRING)

        obj = temp_code_collection.find_one({'temp_code':temp_code})
        '''
        Let this code expire, don't delete it.
        This is so that the user can retry a new password if they get it wrong (too short, etc).
        '''
        if obj and obj['reason'] == PASSWORD_RESET:
            return obj
        temp_code_collection.find_one_and_delete({'temp_code':temp_code})
        return obj

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Public interface
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    def expire_login(self,local_login):
        return self._expire_credentials(local_login)

    def delete_login(self,local_login):
        return self._expire_credentials(local_login,delete=True)

    '''
    logout() requires JWT key expiry. See the JWT interface for this method.
    login() method below should be called before the JWT login() method,
    before JWT keys are generated.
    '''
    def login(self,local_login:str,password:str):
        obj = self._find_credentials(local_login)
        if not obj:
            return False
        if verify_hash(self.logger,obj['password'],password):
            self.logger.warning(f"Local login succeeded: {local_login} .")
            return True

        self.logger.error(f"Login failed for local_login: {local_login} , password failed.")
        return False

    def new_or_existing_user(self,local_login:str =None,password:str =None,
            email:str =None,description:str =None,
            expires_timestamp_seconds:int =None):
        if (local_login in ("",None)) or \
            (email and (('@' not in email) or ('.' not in email))):
            self.logger.error(f'Rejecting new_or_existing_user. Variables are missing/incorrect: local_login: {local_login}, email: {email}')
            return False,False
        self.logger.warning(f'New user created, or user modified: local_login: {local_login}, email: {email}, description {description}')
        return self._save_credentials(local_login,password,email,
            description,expires_timestamp_seconds)

    def generate_temporary_code(self,local_login=None,reason=USER_VERIFICATION):
        return self._gen_temp_code(local_login,reason)

    def verify_temporary_code(self,temp_code):
        obj = self._find_temp_code(temp_code)
        if not obj:
            self.logger.error(f'Temporary code not found: {temp_code}')
            return None,None,None
        return obj['local_login'],obj['reason']

    def change_password(self,local_login:str,password1:str,
        password2:str):
        self.logger.info(f"local_login:{local_login},passwords:{password1} {password2}")
        if password1 != password2:
            self.logger.error(f"password 1 and 2 were not equal, rejecting")
            return False
        if password1 in (None,''):
            self.logger.error(f"password was empty, rejecting")
            return False
        lp1 = len(password1)
        if (lp1 < 9) or (lp1 > 100):
            self.logger.error(f"password was too short or too long, rejecting")
            return False
        if (local_login in (None,"")):
            self.logger.error(f"login was empty, rejecting")
            return False
        ll1 = len(local_login)
        if (ll1 < 4) or (ll1 > 100):
            self.logger.error(f"login was too short or too long, rejecting")
            return False

        obj = self._find_credentials(local_login)
        if not obj:
            self.logger.error(f"change password failed, login not found or expired: local_login {local_login}")
            return False

        self.logger.warning(f"User should be changing password successfully: local_login {local_login}")
        result,is_new = self._save_credentials(obj['local_login'],password1)
        return result

    def find_user(self,local_login:str):
        obj = self._find_credentials(local_login)
        if obj:
            return True
        return False

    def send_verification_email(self,local_login:str,link:str):
        obj = self._find_credentials(local_login)
        if not obj:
            return False
        subject = "Verify your email by clicking this link"
        html = f"""
It looks like you have requested a password reset on the Upstage Authentication Service.<br/>
<br/>
Here's your user verification link: <a href="{link}">{link}</a><br/>
<br/>
Clicking on this link will take you to a Password Reset page, if your verification Code did not expire.<br/>
<br/>
If you did not request this password reset link, please contact us and let us know.<br/>
<br/>
        """
        return sendgrid_send_email(self.logger, [obj['email']], subject, html)

if __name__ == '__main__':
    #import pdb;pdb.set_trace()
    import time
    from loguru import logger
    li = LoginInterface(logger)
    local_login='test'
