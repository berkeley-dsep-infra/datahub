#!/usr/bin/env python3
import logging
import datetime
import argparse
import tempfile
import subprocess
from copy import deepcopy
import time

from .calendar import get_events, _event_repr

# imports needed for vendored _get_cal_tz:
from ruamel.yaml import YAML

yaml = YAML(typ="safe")

UTC = datetime.timezone.utc


def make_deployment(pool_name, template, node_selector, resources, replicas):
    deployment_name = f"{pool_name}-placeholder"
    deployment = deepcopy(template)
    deployment["metadata"]["name"] = deployment_name
    deployment["spec"]["replicas"] = replicas
    deployment["spec"]["template"]["spec"]["nodeSelector"] = node_selector
    deployment["spec"]["template"]["spec"]["containers"][0]["resources"] = resources

    return deployment


log = logging.getLogger(__name__)


def get_replica_counts(events):
    replica_counts = {}
    for ev in events:
        logging.info(f'Found event {_event_repr(ev)}')
        if ev.description:
            try:
                pools_replica_config = yaml.load(ev.description)
            except:
                logging.error(f'Error in parsing description of {_event_repr(ev)}')
                pass
            for pool_name, count in pools_replica_config.items():
                if not isinstance(count, int):
                    continue
                if pool_name not in replica_counts:
                    replica_counts[pool_name] = count
                else:
                    replica_counts[pool_name] = max(replica_counts[pool_name], count)
    return replica_counts


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config-file", default="config.yaml")
    argparser.add_argument("--placeholder-template-file", default="placeholder-template.yaml")

    args = argparser.parse_args()

    while True:
        # Reload all config files on each iteration, so we can change config
        # without needing to bounce the pod
        with open(args.config_file) as f:
            config = yaml.load(f)

        with open(args.placeholder_template_file) as f:
            placeholder_template = yaml.load(f)

        replica_count_overrides = get_replica_counts(get_events(config["calendarUrl"]))
        logging.info(f'Overrides: {replica_count_overrides}')

        # Generate deployment config based on our config
        for pool_name, pool_config in config["nodePools"].items():
            replica_count = max(pool_config["replicas"], replica_count_overrides.get(pool_name, 0))
            deployment = make_deployment(
                pool_name,
                placeholder_template,
                pool_config["nodeSelector"],
                pool_config["resources"],
                replica_count
            )
            logging.info(f'Setting {pool_name} to have {replica_count} replicas')
            with tempfile.NamedTemporaryFile(mode="w") as f:
                yaml.dump(deployment, f)
                f.flush()
                logging.info(subprocess.check_output(["kubectl", "apply", "-f", f.name]).decode().strip())

        time.sleep(60)
