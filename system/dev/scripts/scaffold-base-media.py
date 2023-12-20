import os
import sys
import shutil
from graphql_server import json_encode

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '../../..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)
    
from sqlalchemy import not_
from asset.models import Asset, AssetType, Stage, StageAttribute
from licenses.models import AssetLicense, AssetUsage
from performance_config.models import ParentStage, Performance, Scene
from user.models import User
from event_archive.db import build_pg_session
from event_archive.models import Event
from terminal_colors import bcolors
from config.settings import UPLOAD_USER_CONTENT_FOLDER, ENV_TYPE
from auth.fernet_crypto import encrypt

'''
if ENV_TYPE == 'Production':
    print(bcolors.FAIL + "This script is not meant to be run in production." + bcolors.ENDC)
    exit()
'''

demo_media_folder = 'ui/static/demo'
owner_id = 0

while not os.path.exists(demo_media_folder):
    demo_media_folder = input(bcolors.WARNING + "The folder \"{}\" does not exist. Please put all demo media you wish to scaffold inside that folder, or enter a custom folder to scaffold from: ".format(demo_media_folder) + bcolors.ENDC)

session = build_pg_session()

while not owner_id:
    username = input(bcolors.BOLD + "Please enter the username of the owner whose these base media belong to: " + bcolors.ENDC)
    owner = session.query(User).filter(User.username == username).first()
    if not owner:
        print("❌ The user \"{}\" does not exist.".format(username))
    else:
        owner_id = owner.id

def scan_demo_folder():
    for type in os.listdir(demo_media_folder):
        if '.' not in type:
            for media in os.listdir("{}/{}".format(demo_media_folder, type)):
                yield type, media

created_media_ids = []
upload_assets_folder = '{}'.format(UPLOAD_USER_CONTENT_FOLDER)

def copy_file(src_path, dest_path, type):
    if not os.path.exists(os.path.join(upload_assets_folder, type)):
        os.makedirs(os.path.join(upload_assets_folder, type))
    shutil.copyfile(src_path, os.path.join(upload_assets_folder, dest_path))

def create_media(type, path):
    asset_type = session.query(AssetType).filter(AssetType.name == type).first()
    if not asset_type:
        asset_type = AssetType(name=type)
        session.add(asset_type)
        session.commit()

    asset = Asset(asset_type=asset_type, owner_id=owner_id)
    attributes = {}
    if '.' in path:
        asset.name = os.path.basename(path).split('.')[0]
        # copy asset to uploads folder
        src_path = os.path.join(demo_media_folder, type, path)
        dest_path = os.path.join(type, path)
        copy_file(src_path, dest_path, type)
        asset.file_location = dest_path
    else:
        attributes['multi'] = True
        asset.name = path
        for frame in os.listdir(os.path.join(demo_media_folder, type, path)):
            src_path = os.path.join(demo_media_folder, type, path, frame)
            dest_path = os.path.join(type, "{}_{}".format(path, frame))
            copy_file(src_path, dest_path, type)
            if not asset.file_location:
                asset.file_location = dest_path
                attributes['frames'] = []
            attributes['frames'].append(dest_path)
    asset.description = json_encode(attributes)
    session.add(asset)
    session.commit()
    created_media_ids.append(asset.id)
    print("✅ Created{} {} {}".format(' multi-frame' if 'multi' in attributes else '', type, path))

def create_demo_media():
    for type, path in scan_demo_folder():
        create_media(type, path)

def create_demo_stage():
    if session.query(Stage).filter(Stage.name == 'Demo').first():
        print("❌ A stage named \"Demo\" already exists.")
        return
    stage = Stage(name='Demo Stage', owner_id=owner_id, description='This is a demo stage to help you learn how to use and customise UpStage for your own performances.', file_location='demo')
    status = StageAttribute(name='status', description='live', stage=stage)
    stage.attributes.append(status)
    session.add(stage)
    session.commit()
    for media_id in created_media_ids:
        session.add(ParentStage(stage_id=stage.id, child_asset_id=media_id))
    session.commit()
    print("✅ Created demo stage")

def create_demo_users():
    count = input(bcolors.BOLD + "How many users would you like to create? (type 0 if you don't want to): " + bcolors.ENDC)
    if not count:
        count = 0
    test_user_password = '12345678'
    for i in range(int(count)):
        user = User()
        user.username = "user{}".format(i + 1)
        user.password = encrypt(test_user_password)
        user.email = "user{}@none.none".format(i + 1)
        user.active = True
        session.add(user)
        session.commit()
        print("✅ Created user \"{}\" with password \"{}\"".format(user.username, test_user_password))

create_demo_media()
create_demo_stage()
create_demo_users()
