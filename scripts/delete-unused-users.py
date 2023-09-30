#!/usr/bin/env python3
"""
Delete unused users from a JupyterHub.

JupyterHub performance sometimes scales with *total* number
of users, rather than running number of users. While that should
be fixed, we can work around it by deleting unused users once in
a while. This script will delete anyone who hasn't registered
any activity in a given period of time, double checking to
make sure they aren't active right now. This will require users to
log in again the next time they use the hub, but that's probably
ok.

Core functionality from @minrk:
https://discourse.jupyter.org/t/is-there-a-way-to-bulk-delete-old-users/20866/3
"""
import argparse
import asyncio
from datetime import timedelta, datetime
from dateutil.parser import parse
from jhub_client.api import JupyterHubAPI
import logging
import os
import requests
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logger = logging.getLogger(__name__)

token = os.environ["JUPYTERHUB_API_TOKEN"]
headers = {
    "Accept": "application/jupyterhub-pagination+json",
    "Authorization": f"Bearer {token}",
}

def retrieve_users(hub_url):
    """Returns generator of user models that should be deleted"""
    url = hub_url.rstrip("/") + "/hub/api/users"
    next_page = True
    params = {}

    while next_page:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        resp = r.json()
        user_list = resp["items"]
        for user in user_list:
            # only yield users that should be deleted
            if should_delete(user):
                yield user

        pagination = resp["_pagination"]
        next_page = pagination["next"]
        if next_page:
            params = {
                "offset": next_page["offset"],
                "limit": next_page["limit"],
            }

def should_delete(user):
    """
    Returns a boolean if user is to be deleted.  The critera are:
      - was the user active in the past 24 hours?
      - is there a current user server running?
    """
    last_activity_str = user.get('last_activity', False)
    if last_activity_str:
        try:
            last_activity = parse(user['last_activity'])
        except:
            logger.error(f"Unexpected value for user['last_activity']: {user['last_activity']}")
            raise
        if isinstance(last_activity, datetime):
            was_active_last_day = datetime.now().astimezone() - last_activity < timedelta(hours=24)
        else:
            logger.error(f"For user {user['name']}, expected datetime.datetime class for last_activity but got {type(last_activity)} instead.")
            raise

        logger.debug(f"User: {user['name']}")
        logger.debug(f"Last login: {last_activity}")
        logger.debug(f"24hrs since last login: {was_active_last_day}")
        logger.debug(f"Running server: {user['server']}")
        if was_active_last_day or user['server'] is not None:
            logger.info(f"Not deleting {user['name']}")
            return False
        else:
            logger.info(f"Flagged {user['name']} for deletion.")
            return True

def delete_user(hub_url, name):
    """Delete a given user by name via JupyterHub API"""
    r = requests.delete(
        hub_url.rstrip("/") + f"/hub/api/users/{name}",
        headers=headers,
    )
    r.raise_for_status()

def main(args):
    """
    Get users from a hub, check to see if they should be deleted from the ORM
    and if so, delete them!
    """
    count = 1
    for user in list(retrieve_users(args.hub_url)):
        print(f"{count}: deleting {user['name']}")
        if not args.dry_run:
            delete_user(args.hub_url, user['name'])
            count += 1
    else:   
            logger.warning(f"Skipped {user['name']} due to dry run.")
            # await delete_user(hub, user, count)

    count -= 1
    print(f"Deleted {count} total users.")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--hub_url',
        help='Fully qualified URL to the JupyterHub',
        required=True
    )
    argparser.add_argument(
        '--dry_run',
        action='store_true',
        help='Dry run without deleting users'
    )
    argparser.add_argument(
        '-v',
        dest='verbose',
        action='store_true',
        help='Set info log level'
    )
    argparser.add_argument(
        '-d',
        dest='debug',
        action='store_true',
        help='Set debug log level'
    )
    args = argparser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)
    elif args.debug:
        logger.setLevel(logging.DEBUG)

    main(args)
