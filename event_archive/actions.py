import logging
import json
import os
import sys

import config as conf
from system import reacts_to_payload, reacts_to_anything
from db import build_pg_session
from models import Event


@reacts_to_anything
def record_event(performance_id, payload, timestamp):
    session = None
    try:
        session = build_pg_session()
        event = Event(performance_id=performance_id, payload=payload, mqtt_timestamp=timestamp)
        session.add(event)
        session.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if session is not None:
            session.close()

    
