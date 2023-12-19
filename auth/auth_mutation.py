from config.project_globals import app, DBSession, ScopedSession
from auth.fernet_crypto import encrypt, decrypt
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                create_access_token, create_refresh_token,
                                verify_jwt_in_request, JWTManager)
from user.models import OneTimeTOTP, User
from auth.models import UserSession
from auth.auth_api import TNL
from flask import request
import sys
import os
import graphene
import pyotp

from mail.mail_utils import send
from mail.templates import password_reset
appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


jwt = JWTManager(app)


class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise Exception('Authenication Failure : User is not registered')
        if decrypt(password) != user.password:
            raise Exception('Authenication Failure : Bad Password')
        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username)
        )
        # TODO: Add session handling, etc.


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @jwt_required(refresh=True)
    def mutate(self, info, refresh_token):
        current_user_id = get_jwt_identity()
        refresh_token = request.headers[app.config['JWT_HEADER_NAME']]

        user = DBSession.query(User).filter(User.id == current_user_id
                                            ).filter(User.active == True).first()

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


class RequestPasswordResetMutation(graphene.Mutation):
    class Arguments(object):
        username_or_email = graphene.String()

    message = graphene.String()
    username = graphene.String()

    def mutate(self, info, username_or_email):
        with ScopedSession() as local_db_session:
            if '@' in username_or_email:
                user = local_db_session.query(User).filter(
                    User.email == username_or_email).first()
            else:
                user = local_db_session.query(User).filter(
                    User.username == username_or_email).first()

            if user:
                email = user.email
                username = user.username
            else:
                raise Exception(
                    f"We cannot find any user with this {'email' if '@' in username_or_email else 'username'}!")

            totp = pyotp.TOTP(pyotp.random_base32())
            otp = totp.now()

            local_db_session.query(OneTimeTOTP).filter(
                OneTimeTOTP.user_id == user.id).delete()
            local_db_session.flush()
            local_db_session.add(OneTimeTOTP(user_id=user.id, code=otp))
            local_db_session.flush()
            send(email, f"Password reset for account {user.username}", password_reset(user, otp))

        return RequestPasswordResetMutation(
            message=f"We've sent an email with a code to reset your password to {email}.",
            username=username
        )


class VerifyPasswordResetMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        otp = graphene.String()

    message = graphene.String()

    def mutate(self, info, username, otp):
        with ScopedSession() as local_db_session:
            user = local_db_session.query(User).filter(
                User.username == username).first()

            if not user:
                raise Exception(
                    f"We cannot find any user with this username!")

            otp_record = local_db_session.query(OneTimeTOTP).filter(
                OneTimeTOTP.user_id == user.id).first()

            if not otp_record or otp_record.code != otp:
                raise Exception(
                    f"Invalid OTP code. Please try again.")

            return VerifyPasswordResetMutation(message=f"Valid OTP code. Please enter a new password.")


class PasswordResetMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        otp = graphene.String()
        password = graphene.String()

    message = graphene.String()

    def mutate(self, info, username, otp, password):
        with ScopedSession() as local_db_session:
            user = local_db_session.query(User).filter(
                User.username == username).first()

            if not user:
                raise Exception(
                    f"We cannot find any user with this username!")

            otp_record = local_db_session.query(OneTimeTOTP).filter(
                OneTimeTOTP.user_id == user.id).first()

            if not otp_record or otp_record.code != otp:
                raise Exception(
                    f"Invalid OTP code. Please try again.")

            local_db_session.query(OneTimeTOTP).filter(
                OneTimeTOTP.user_id == user.id).delete()
            user.password = encrypt(password)
            local_db_session.flush()

            return PasswordResetMutation(message=f"Password reset successfully.")
