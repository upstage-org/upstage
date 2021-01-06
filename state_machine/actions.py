import logging
import os
import sys

import config as conf
from system import reacts_to_payload, reacts_to_anything
from db import build_client


def get_state(performance_id):
    client = build_client()
    db = client[conf.MONGO_DB]
    state = None
    while state is None:
        state = db[conf.PERFORMANCE_STATE_COLLECTION].find_one(
            {"performance_id": performance_id}
        )
        if state is None:
            db[conf.PERFORMANCE_STATE_COLLECTION].insert_one(
                {"performance_id": performance_id, "avatars": {}}
            )
    client.close()
    return state


def save_state(state):
    client = build_client()
    db = client[conf.MONGO_DB]
    db[conf.PERFORMANCE_STATE_COLLECTION].replace_one({"_id": state["_id"]}, state)
    client.close()


@reacts_to_payload("type=placeAvatarOnStage")
def place_avatar_on_stage(performance_id, payload, timestamp):
    state = get_state(performance_id)
    details = payload["details"]
    state["avatars"][details["id"]] = {
        "src": details["src"],
        "x": details["x"],
        "y": details["y"],
    }
    save_state(state)


@reacts_to_payload("type=moveTo")
def move_avatar_to(performance_id, payload, timestamp):
    state = get_state(performance_id)
    try:
        details = payload["details"]
        state["avatars"][details["id"]]["x"] = details["x"]
        state["avatars"][details["id"]]["y"] = details["y"]
        save_state(state)
    except:
        pass


@reacts_to_anything
def record_event(performance_id, payload, timestamp):
    client = build_client()
    db = client[conf.MONGO_DB]
    db[f"{performance_id}_archive"].insert_one(
        {"payload": payload, "timestamp": timestamp}
    )
