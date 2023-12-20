import os
import sys

import pathlib

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from sqlalchemy import not_
from core.asset.models import Asset, Stage, StageAttribute, MediaTag
from core.licenses.models import AssetLicense, AssetUsage
from core.performance_config.models import ParentStage, Performance, Scene
from core.event_archive.db import build_pg_session
from core.event_archive.models import Event
from terminal_colors import bcolors
from config import UPLOAD_USER_CONTENT_FOLDER


stages_to_be_kepts = ["8thMarch"]

print(
    bcolors.WARNING
    + "Are you sure you want to do the clean up? This will delete all stages except {0}!".format(
        stages_to_be_kepts
    )
    + bcolors.ENDC
)
print(
    'If you want to keep any stages, please add them to the "stages_to_be_kepts" list in "scripts/wipe_dev.py".'
)

if input(bcolors.BOLD + 'Type "confirm" to continue: ' + bcolors.ENDC) != "confirm":
    print(bcolors.FAIL + "Aborted!" + bcolors.ENDC)
    sys.exit(0)

print(bcolors.OKGREEN + "Start cleaning up..." + bcolors.ENDC)
session = build_pg_session()

with session.no_autoflush:
    keep_ids = []
    for stage in session.query(Stage).all():
        if stage.file_location in stages_to_be_kepts:
            keep_ids.append(stage.id)

    session.query(ParentStage).filter(ParentStage.stage_id.notin_(keep_ids)).delete(
        synchronize_session=False
    )

    for asset in session.query(Asset).filter(not_(Asset.stages.any())).all():
        print("🗑️ Deleting asset: {}".format(asset.name))
        session.query(AssetLicense).filter(AssetLicense.asset_id == asset.id).delete(
            synchronize_session=False
        )
        session.query(AssetUsage).filter(AssetUsage.asset_id == asset.id).delete(
            synchronize_session=False
        )
        session.query(MediaTag).filter(MediaTag.asset_id == asset.id).delete(
            synchronize_session=False
        )
        session.delete(asset)

    upload_assets_folder = "{}".format(UPLOAD_USER_CONTENT_FOLDER)

    for ftype in os.listdir(upload_assets_folder):
        if ("." not in ftype) and (".." not in ftype) and os.path.isdir(ftype):
            for media in os.listdir("{}/{}".format(upload_assets_folder, ftype)):
                if (
                    not session.query(Asset)
                    .filter(Asset.file_location == "{}/{}".format(ftype, media))
                    .first()
                ):
                    print("🗑️ Deleting file {}/{}".format(ftype, media))
                    try:
                        pathlib.Path(
                            "{}/{}/{}".format(upload_assets_folder, ftype, media)
                        ).unlink()
                    except:
                        print(
                            "Failed to remove {}/{}/{}".format(
                                upload_assets_folder, ftype, media
                            )
                        )

    for stage in session.query(Stage).all():
        if stage.file_location not in stages_to_be_kepts:
            print("🗑️ Deleting stage: {}".format(stage.name))
            session.query(StageAttribute).filter(
                StageAttribute.stage_id == stage.id
            ).delete(synchronize_session=False)
            sample_event = (
                session.query(Event)
                .filter(
                    Event.performance_id.in_(
                        session.query(Performance.id).filter(
                            Performance.stage_id == stage.id
                        )
                    )
                )
                .first()
            )
            if sample_event:
                session.query(Event).filter(Event.topic == sample_event.topic).delete(
                    synchronize_session=False
                )
            session.query(Performance).filter(Performance.stage_id == stage.id).delete(
                synchronize_session=False
            )
            session.query(Scene).filter(Scene.stage_id == stage.id).delete(
                synchronize_session=False
            )
            session.delete(stage)
        else:
            print("🗑️ Clearing replays and scenes of {}".format(stage.name))
            session.query(Performance).filter(Performance.stage_id == stage.id).delete(
                synchronize_session=False
            )
            session.query(Scene).filter(Scene.stage_id == stage.id).delete(
                synchronize_session=False
            )

session.commit()
session.close()

print("Done!")
