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
"""
import argparse
from jhub_client.api import JupyterHubAPI
from dateutil.parser import parse
import asyncio
from datetime import timedelta, datetime

async def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'hub_url',
        help='Fully qualified URL to the JupyterHub'
    )
    argparser.add_argument(
        '--dry_run',
        action='store_true',
        help='Dry run without deleting users'
    )
    args = argparser.parse_args()

    to_delete = []
    async with JupyterHubAPI(hub_url=args.hub_url) as hub:
        users = await hub.list_users()
        for user in users:
            last_activity_str = user.get('last_activity', False)
            if last_activity_str:
                try:
                    last_activity = parse(user['last_activity'])
                except:
                    print(user['last_activity'])
                    raise

                if isinstance(last_activity, datetime):
                    was_active_last_day = datetime.now().astimezone() - last_activity < timedelta(hours=24)
                else:
                    activity_type = type(last_activity)
                    print(f"expected datetime.datetime class for last_activity, got {activity_type} instead.")
                    raise

                print(f"User: {user['name']}")
                print(f"Last login: {last_activity}")
                print(f"24hrs since last login: {was_active_last_day}")
                print(f"Running server: {user['server']}")
                if (last_activity and was_active_last_day) or (user['server'] is not None):
                    print(f"Not deleting {user['name']}")
                else:
                    to_delete.append(user['name'])
                    print(f"Deleting {user['name']}")
                print("")

        for i, username in enumerate(to_delete):
            print(f'{i+1} of {len(to_delete)}: deleting {username}')
            if not args.dry_run:
                await hub.delete_user(username)
            else:
                print('Skipped due to dry run.')

if __name__ == '__main__':
    asyncio.run(main())
