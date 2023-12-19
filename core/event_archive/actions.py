import logging
import json
import os
import sys

from core.event_archive.system import reacts_to_payload, reacts_to_anything
from core.event_archive.db import build_pg_session
from core.event_archive.models import Event


@reacts_to_anything
def record_event(topic, payload, timestamp):
    if topic.endswith("statistics"):
        return  # Statistic should be in realtime, record it just make our event archive heavier
    session = None
    try:
        session = build_pg_session()
        event = Event(topic=topic, payload=payload, mqtt_timestamp=timestamp)
        session.add(event)
        session.commit()
    except Exception as error:
        logging.error(error)
    finally:
        if session is not None:
            session.close()
