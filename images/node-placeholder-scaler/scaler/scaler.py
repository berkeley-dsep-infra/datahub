#!/usr/bin/env python3
import logging
import datetime
import argparse
import tempfile
import subprocess
import requests
import os
from copy import deepcopy
import time

from .calendar import get_calendar, get_events, _event_repr

from ruamel.yaml import YAML
yaml = YAML(typ="safe")


def make_deployment(pool_name, template, node_selector, resources, replicas):
    deployment_name = f"{pool_name}-placeholder"
    deployment = deepcopy(template)
    deployment["metadata"]["name"] = deployment_name
    deployment["spec"]["replicas"] = replicas
    deployment["spec"]["template"]["spec"]["nodeSelector"] = node_selector
    deployment["spec"]["template"]["spec"]["containers"][0]["resources"] = resources

    return deployment


log = logging.getLogger(__name__)


def post_grafana_annotation(grafana_url, grafana_api_key, tags, text):
    """
    Create annotation in a grafana instance.
    """
    return requests.post(
        grafana_url + "/api/annotations",
        json={
            "tags": tags,
            "text": text,
            "time": int(time.time() * 1000),
            "isRegion": False,
        },
        headers={"Authorization": f"Bearer {grafana_api_key}"},
    ).text


def get_replica_counts(events):
    replica_counts = {}
    for ev in events:
        logging.info(f"Found event {_event_repr(ev)}")
        if ev.description:
            # initialize
            pools_replica_config = None
            try:
                pools_replica_config = yaml.load(ev.description)
            except:
                logging.error(f"Error in parsing description of {_event_repr(ev)}")
                logging.error(f"{ev.description=}")
                pass
            if pools_replica_config is None:
                logging.error(f"No description in event {_event_repr(ev)}")
                continue
            elif type(pools_replica_config) == str:
                logging.error(f"Event description not parsed as dictionary.")
                logging.error(f"{ev.description=}")
                continue
            for pool_name, count in pools_replica_config.items():
                if not isinstance(count, int):
                    logging.info(f"Count {count} not an integer.")
                    continue
                if pool_name not in replica_counts:
                    replica_counts[pool_name] = count
                else:
                    replica_counts[pool_name] = max(replica_counts[pool_name], count)
        else:
            logging.error(f"Event has no description: {_event_repr(ev)}")
    return replica_counts


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config-file", default="config.yaml")
    argparser.add_argument(
        "--placeholder-template-file", default="placeholder-template.yaml"
    )

    args = argparser.parse_args()

    while True:
        # Reload all config files on each iteration, so we can change config
        # without needing to bounce the pod
        with open(args.config_file) as f:
            config = yaml.load(f)

        with open(args.placeholder_template_file) as f:
            placeholder_template = yaml.load(f)

        calendar = get_calendar(config["calendarUrl"])
        events = get_events(calendar)
        logging.info(f"Found {len(events)} events at {config['calendarUrl']}.")

        replica_count_overrides = get_replica_counts(events)
        logging.info(f"Overrides: {replica_count_overrides}")

        actions_taken = []

        # Generate deployment config based on our config
        for pool_name, pool_config in config["nodePools"].items():
            replica_count = replica_count_overrides.get(
                pool_name, pool_config["replicas"]
            )
            deployment = make_deployment(
                pool_name,
                placeholder_template,
                pool_config["nodeSelector"],
                pool_config["resources"],
                replica_count,
            )
            logging.info(f"Setting {pool_name} to have {replica_count} replicas")
            with tempfile.NamedTemporaryFile(mode="r+") as f:
                yaml.dump(deployment, f)
                f.flush()
                proc = subprocess.run(
                    ["kubectl", "apply", "-f", f.name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                logging.info(proc.stdout.strip())

                # the prior logic here was looking for 'deployment.apps/data100-placeholder unchanged',
                # but kubectl always returns 'deployment.apps/data100-placeholder configured'.
                #
                # since that logic always fails, the scaler would spam grafana
                # with a notation for each hub, once a minute, for perpetuity.
                #
                # the 'Find out what happened her' is, i assume, a breadcrumb
                # from yuvi, also leaving me to believe that this never really
                # worked as intended. ;)
                #
                # 'actions_taken' could actually be useful in some way, so i
                # plan on leaving that here (and commented out, most likely,
                # for perpetuity).
                #
                # actions_taken.append(f"{pool_name} set to {replica_count}")
                # Find out what happened her

        if "grafana" in config and actions_taken:
            # Post to grafana if we took any actions
            grafana_url = config["grafana"]["url"]
            grafana_tags = config["grafana"]["tags"]
            grafana_api_key = os.environ["GRAFANA_API_KEY"]
            text = "\n".join(actions_taken)
            post_grafana_annotation(grafana_url, grafana_api_key, grafana_tags, text)
            log.info("Posted annotation to Grafana")

        time.sleep(60)
