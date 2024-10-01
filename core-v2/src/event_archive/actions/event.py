import logging
import json
import os
import sys

from global_config import ScopedSession
from event_archive.db_models.event import EventModel
from event_archive.systems.system import reacts_to_anything


@reacts_to_anything
def record_event(topic, payload, timestamp):
    if topic.endswith("statistics"):
        return  # Statistic should be in realtime, record it just make our event archive heavier
    session = None
    try:
        with ScopedSession() as session:
            event = EventModel(topic=topic, payload=payload, mqtt_timestamp=timestamp)
            session.add(event)
            session.commit()
            session.flush()
    except Exception as error:
        logging.error(error)
    finally:
        if session is not None:
            session.close()
