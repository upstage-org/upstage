import logging
import re
import json
from multiprocessing import Process, cpu_count
import os

from global_config import EVENT_COLLECTION, MONGO_DB
from event_archive.config.mongodb import build_mongo_client


_payload_map = {}
_anything_list = []


def reacts_to_anything(f):
    global _anything_list
    if f not in _anything_list:
        _anything_list.append(f)
    return f


def reacts_to_payload(rules: list = []):
    if not isinstance(rules, list):
        rules = [rules]

    def inner(f):
        global _payload_map
        for r in rules:
            try:
                path, regex = r.split("=")
                re.compile(regex)
                if None in [path, regex]:
                    raise ValueError
                if f not in _payload_map:
                    _payload_map[f] = []
                _payload_map[f].append(r)
            except ValueError:
                raise ValueError(f"{r} is invalid.  Must be: JSON_PATH=REGEX")

    return inner


def get_value_at(payload, path):
    for i in path.split("."):
        if i in payload:
            payload = payload[i]
        else:
            return None
    return payload


def functions_for(payload):
    global _payload_map, _anything_list
    output = _anything_list.copy()
    for f, rules in _payload_map.items():
        if f in output:
            continue
        should_add = True
        for r in rules:
            try:
                path, regex = r.split("=")
                regex = re.compile(regex)
                val = get_value_at(payload, path)
                if not regex.match(val):
                    raise ValueError
            except:
                should_add = False
                break
        if should_add:
            output.append(f)
    return output


def worker():
    logging.info(f"Worker started (PID: {os.getpid()})")
    client = build_mongo_client()
    db = client[MONGO_DB]
    queue = db[EVENT_COLLECTION]
    while True:
        try:
            event = queue.find_one_and_delete({})
            if event:
                logging.info(f"{os.getpid()} Processing: {event}")
                topic = event["topic"]
                payload = json.loads(event["payload"])
                timestamp = event["timestamp"]
                funcs = functions_for(payload)
                for f in funcs:
                    f(topic, payload, timestamp)
        except Exception as e:
            logging.error(e)
    logging.info("Worker exited")


def run():
    processes = [Process(target=worker, args=()) for _ in range(cpu_count())]
    logging.info(f"Spawning {len(processes)} processes...")
    for p in processes:
        p.start()
