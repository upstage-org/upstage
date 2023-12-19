#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
import os, sys
import pyotp
import qrcode

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.project_globals import DBSession, Base, metadata, engine, ScopedSession, app
from config import ENV_TYPE, URL_PREFIX

from core.user.models import User, OneTimeTOTP


def generate_user_totp(user_id):
    user = DBSession.query(User).filter(User.id == user_id).one()
    local_db_session = get_scoped_session()

    local_db_session.query(OneTimeTOTP).filter(OneTimeTOTP.user_id == user_id).delete(
        synchronize_session=False
    )

    code = pyotp.random_base32()

    totp_record = OneTimeTOTP(
        user_id=user_id,
        url=f"otpauth://totp/UPSTAGE_{ENV_TYPE}:{user.email}?secret={code}&issuer=Upstage",
        code=code,
    )

    local_db_session.add(totp_record)
    local_db_session.flush()
    totp_record_url = totp_record.url
    local_db_session.commit()
    local_db_session.close()

    img = qrcode.make(totp_record_url)
    fname = "/tmp/{}_{}_{}.png".format(user_id, user.email, "gauth")
    img.save(fname)


def verify_user_totp(user, num_value):
    totp_record = (
        DBSession.query(OneTimeTOTP).filter(OneTimeTOTP.user_id == user.id).first()
    )
    if not totp_record:
        app.logger.warning("User's totp record does not exist:{}".format(user.id))
        return False
    totp = pyotp.TOTP(totp_record.code)
    result = totp.verify(num_value)
    # print("TOTP user: {} code:{} num:{} result:{}".format(user.id,totp_record.code,num_value,result))
    return result


def one_time_prod_gen():
    if ENV_TYPE != "Production":
        print("Nope.")
        return

    # This will delete and replace codes!!!
    for user in (
        DBSession.query(User)
        .filter(User.active == True)
        .filter(User.role.in_((4, 8)))
        .all()
    ):
        generate_user_totp(user.id)


def dev_harness():
    # Use one TOTP QR and code for all of dev.
    if ENV_TYPE == "Production":
        print("Nope.")
        return

    threesixthree = (
        DBSession.query(OneTimeTOTP).filter(OneTimeTOTP.user_id == 363).one()
    )
    for user in DBSession.query(User).filter(User.role.in_((4, 8))).all():
        if not user.active:
            continue
        if user.id == 363:
            continue
        local_db_session = get_scoped_session()

        totp_record = (
            local_db_session.query(OneTimeTOTP)
            .filter(OneTimeTOTP.user_id == user.id)
            .first()
        )

        if not totp_record:
            totp_record = OneTimeTOTP(
                user_id=user.id,
            )
            local_db_session.add(totp_record)

        totp_record.url = threesixthree.url
        totp_record.code = threesixthree.code

        local_db_session.commit()
        local_db_session.close()

        img = qrcode.make(threesixthree.url)
        fname = "/tmp/UPSTAGE_{}.png".format("gauth")
        img.save(fname)


if __name__ == "__main__":
    # import pdb;pdb.set_trace()
    # one_time_prod_gen()
    pass
    # generate_user_totp(3648)
    # user = DBSession.query(User).filter(User.id==363).one()
    # print(verify_user_totp(user,597076))
