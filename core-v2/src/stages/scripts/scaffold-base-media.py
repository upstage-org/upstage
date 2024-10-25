import os
import sys
import shutil
from graphql_server import json_encode
from PIL import Image

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from assets.db_models.asset_type import AssetTypeModel
from assets.db_models.asset import AssetModel
from stages.db_models.stage import StageModel
from stages.db_models.stage_attribute import StageAttributeModel
from stages.db_models.parent_stage import ParentStageModel
from users.db_models.user import UserModel, ADMIN, GUEST
from upstage_options.db_models.config import ConfigModel
from global_config import encrypt, UPLOAD_USER_CONTENT_FOLDER, global_session

DBSession = global_session


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


"""
if ENV_TYPE == 'Production':
    print(bcolors.FAIL + "This script is not meant to be run in production." + bcolors.ENDC)
    exit()
"""

demo_media_folder = "../../dashboard/demo"
owner_id = 0

while not os.path.exists(demo_media_folder):
    demo_media_folder = input(
        bcolors.WARNING
        + 'The folder "{}" does not exist. Please put all demo media you wish to scaffold inside that folder, or enter a custom folder to scaffold from: '.format(
            demo_media_folder
        )
        + bcolors.ENDC
    )


while not owner_id:
    username = input(
        bcolors.BOLD
        + "Please enter the username of the owner whose these base media belong to: "
        + bcolors.ENDC
    )
    owner = DBSession.query(UserModel).filter(UserModel.username == username).first()
    if not owner:
        print('❌ The user "{}" does not exist.'.format(username))
    else:
        owner_id = owner.id


def scan_demo_folder():
    for type in os.listdir(demo_media_folder):
        if "." not in type:
            for media in os.listdir("{}/{}".format(demo_media_folder, type)):
                yield type, media


created_media_ids = []
upload_assets_folder = "{}".format(UPLOAD_USER_CONTENT_FOLDER)


def copy_file(src_path, dest_path, type):
    if not os.path.exists(os.path.join(upload_assets_folder, type)):
        os.makedirs(os.path.join(upload_assets_folder, type))
    shutil.copyfile(src_path, os.path.join(upload_assets_folder, dest_path))


def detect_size(type, path):
    if type == "stream":
        size = path.split(".")[0].split("_")[-1].split("x")
        if len(size) == 2:
            return down_size(size)
        else:
            print(
                '❌ Please put the video dimension in the stream name, otherwise stream will have square frame. For example "Demo stream_800x600.mp4". Current name: {}{}{}'.format(
                    bcolors.FAIL, path, bcolors.ENDC
                )
            )
            return 100, 100
    else:
        with Image.open(path) as img:
            return down_size(img.size)


def down_size(size):
    w = int(size[0])
    h = int(size[1])
    if w > h:
        h = 100 * h / w
        w = 100
    else:
        w = 100 * w / h
        h = 100
    return w, h


def create_media(type, path):
    asset_type = (
        DBSession.query(AssetTypeModel).filter(AssetTypeModel.name == type).first()
    )
    if not asset_type:
        asset_type = AssetTypeModel(name=type, file_location="")
        DBSession.add(asset_type)
        DBSession.commit()

    asset = AssetModel(asset_type=asset_type, owner_id=owner_id, file_location="")
    attributes = {}
    size = 0
    if "." in path:
        asset.name = os.path.basename(path).split(".")[0]
        # copy asset to uploads folder
        src_path = os.path.join(demo_media_folder, type, path)
        dest_path = os.path.join(type, path)
        print(src_path, dest_path)
        copy_file(src_path, dest_path, type)
        asset.file_location = dest_path
        size += os.path.getsize(src_path)
        if type != "audio" and path[0] != ".":
            attributes["w"], attributes["h"] = detect_size(type, src_path)
    else:
        attributes["multi"] = True
        asset.name = path
        for frame in os.listdir(os.path.join(demo_media_folder, type, path)):
            src_path = os.path.join(demo_media_folder, type, path, frame)
            dest_path = os.path.join(type, "{}_{}".format(path, frame))
            copy_file(src_path, dest_path, type)
            size += os.path.getsize(src_path)
            if not asset.file_location:
                asset.file_location = dest_path
                attributes["frames"] = []
                attributes["w"], attributes["h"] = detect_size(type, src_path)
            attributes["frames"].append(dest_path)

    asset.description = json_encode(attributes)
    asset.size = size
    DBSession.add(asset)
    DBSession.commit()
    created_media_ids.append(asset.id)
    print(
        "✅ Created{} {} {}".format(
            " multi-frame" if "multi" in attributes else "", type, path
        )
    )


def create_demo_media():
    for type, path in scan_demo_folder():
        create_media(type, path)


def create_demo_stage():
    if DBSession.query(StageModel).filter(StageModel.name == "Demo").first():
        print('⏩ A stage named "Demo" already exists.')
        return
    stage = StageModel(
        name="Demo Stage",
        owner_id=owner_id,
        description="This is a demo stage to help you learn how to use and customise UpStage for your own performances.",
        file_location="demo",
    )
    status = StageAttributeModel(name="status", description="live", stage=stage)
    stage.attributes.append(status)

    visibility = StageAttributeModel(name="visibility", description="1", stage=stage)
    stage.attributes.append(visibility)

    cover_src = os.path.join(demo_media_folder, "demo-stage-cover.jpg")
    cover_path = os.path.join("media", "demo-stage-cover.jpg")
    copy_file(cover_src, cover_path, "media")
    cover = StageAttributeModel(name="cover", description=cover_path, stage=stage)
    stage.attributes.append(cover)

    all_users = [x.id for x in DBSession.query(UserModel.id).all()]
    accesses = [[], all_users]
    player_access = StageAttributeModel(
        name="playerAccess", description=json_encode(accesses), stage=stage
    )
    stage.attributes.append(player_access)

    DBSession.add(stage)
    DBSession.commit()
    for media_id in created_media_ids:
        DBSession.add(ParentStageModel(stage_id=stage.id, child_asset_id=media_id))
    DBSession.commit()
    print("✅ Created demo stage")


def create_demo_users():
    # - Super Admin: with email address support@upstage.live
    # - Guest: one guest account?
    # - Probably no other users as default
    admin_username = "admin"
    guest_username = "guest"
    admin_email = "support@upstage.live"
    guest_email = "guest@upstage.live"
    test_user_password = "12345678"

    if (
        DBSession.query(UserModel).filter(UserModel.username == admin_username).first()
        or DBSession.query(UserModel).filter(UserModel.email == admin_email).first()
    ):
        print('⏩ An admin user with email "{}" already exists.'.format(admin_email))
    else:
        admin = UserModel()
        admin.username = admin_username
        admin.password = encrypt(test_user_password)
        admin.email = admin_email
        admin.role = ADMIN
        admin.active = True
        DBSession.add(admin)
        print(
            '✅ Created admin account with credentials: "{}" and password "{}"'.format(
                admin_username, test_user_password
            )
        )

    if (
        DBSession.query(UserModel).filter(UserModel.username == guest_username).first()
        or DBSession.query(UserModel).filter(UserModel.email == guest_email).first()
    ):
        print('⏩ A guest user with email "{}" already exists.'.format(guest_username))
    else:
        guest = UserModel()
        guest.username = guest_username
        guest.password = encrypt(test_user_password)
        guest.email = guest_email
        guest.role = GUEST
        guest.active = True
        DBSession.add(guest)
        print(
            '✅ Created guest account with credentials: "{}" and password "{}"'.format(
                guest_username, test_user_password
            )
        )

    DBSession.commit()


def save_config(name, value):
    config = DBSession.query(ConfigModel).filter(ConfigModel.name == name).first()
    if config:
        config.value = value
    else:
        config = ConfigModel(name=name, value=value)
        DBSession.add(config)
    DBSession.commit()


def scaffold_foyer():
    save_config("FOYER_TITLE", "Your New UpStage")
    save_config(
        "FOYER_DESCRIPTION",
        "Welcome to your new UpStage! Log in to get started.",
    )
    print("✅ Foyer Scaffolding Completed")


def scaffold_system_configuration():
    save_config(
        "TERMS_OF_SERVICE",
        "https://raw.githubusercontent.com/upstage-org/upstage/main/LICENSE",
    )
    save_config("MANUAL", "https://docs.upstage.live")
    print("✅ System Configuration Scaffolding Completed")


create_demo_media()
create_demo_stage()
create_demo_users()
scaffold_foyer()
scaffold_system_configuration()
