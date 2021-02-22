import sys,os
import graphene

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask_jwt_extended import (jwt_required,get_jwt_identity,
    create_access_token,create_refresh_token,
    verify_jwt_in_request,JWTManager)

from config.project_globals import app
from auth.fernet_crypto import encrypt,decrypt
from auth.auth_api import TNL
from user.models import User

jwt = JWTManager(app)

class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()
    
    def mutate(self, info , username, password) :
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            raise Exception('Authenication Failure : User is not registered')
        if decrypt(password.lower()) != user.password:
            raise Exception('Authenication Failure : Bad Password')
        return AuthMutation(
            access_token = create_access_token(username),
            refresh_token = create_refresh_token(username)
        )
        # TODO: Add session handling, etc.

class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @jwt_required(refresh=True)
    def mutate(self):
        current_user_id = get_jwt_identity()
        refresh_token = request.headers[app.config['JWT_HEADER_NAME']]

        user = DBSession.query(User).filter(User.id==current_user_id
            ).filter(User.active==True).first()

        if not user:
            TNL.add(refresh_token)
            raise Exception("Your session expired. Please log in again.")

        access_token = create_access_token(identity=current_user_id)

        user_session = UserSession(
            user_id=current_user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            app_version=request.headers.get('X-Upstage-App-Version'),
            app_os_type=request.headers.get("X-Upstage-Os-Type"),
            app_os_version=request.headers.get("X-Upstage-Os-Version"),
            app_device=request.headers.get("X-Upstage-Device-Model")
        )

        with ScopedSession() as local_db_session:
            local_db_session.add(user_session)
            local_db_session.flush()
            user_session_id = user_session.id

        return RefreshMutation(new_token=access_token)


