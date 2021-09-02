#!/usr/bin/env python3
import logging
import datetime

import icalendar
import requests
from icalevents import icalevents

# imports needed for vendored _get_cal_tz:
from dateutil.tz import gettz
from pytz import timezone

from ruamel.yaml import YAML

yaml = YAML(typ="safe")

UTC = datetime.timezone.utc

log = logging.getLogger(__name__)

def utcnow():
    """Standalone function for easier mocking"""
    return datetime.datetime.now(tz=datetime.timezone.utc)



def _event_repr(event):
    """
    Simple repr of a calenar event

    For use in logging. Shows title and time.
    """
    if event.all_day:
        return f"{event.summary} {event.start.date()}"
    else:
        if event.end.date() == event.start.date():
            return f"{event.summary} {event.start.strftime('%Y-%m-%d %H:%M')}-{event.end.strftime('%H:%M')}"
        else:
            return f"{event.summary} {event.start.strftime('%Y-%m-%d %H:%M')}-{event.end.strftime('%Y-%m-%d %H:%M')}"


def _get_cal_tz(content: str):
    """
    Get the calendar timezone

    This code is extracted from icalevents.icalparser
    It's not in an importable form over there, so copy it outright

    License: MIT
    """
    calendar = icalendar.Calendar.from_ical(content)

    # BEGIN PATCH: support X-WR-Timezone, which google sets as calendar default timezone
    if calendar.get("x-wr-timezone"):
        return gettz(str(calendar["x-wr-timezone"]))
    # END PATCH

    # Keep track of the timezones defined in the calendar
    timezones = {}
    for c in calendar.walk("VTIMEZONE"):
        name = str(c["TZID"])
        try:
            timezones[name] = c.to_tz()
        except IndexError:
            # This happens if the VTIMEZONE doesn't
            # contain start/end times for daylight
            # saving time. Get the system pytz
            # value from the name as a fallback.
            timezones[name] = timezone(name)

    # If there's exactly one timezone in the file,
    # assume it applies globally, otherwise UTC
    if len(timezones) == 1:
        cal_tz = gettz(list(timezones)[0])
    else:
        cal_tz = UTC
    return cal_tz


def get_events(url: str):
    """
    Wrapper for icalevents.events

    Mostly to deal with weird issues around url parsing and timezones
    """

    if url.startswith("file://"):
        path = url.split("://", 1)[1]
        with open(path) as f:
            content = f.read()
    elif "://" not in url:
        path = url
        with open(path) as f:
            content = f.read()
    else:
        r = requests.get(url)
        r.raise_for_status()
        content = r.text

    cal_tz = _get_cal_tz(content)

    now = utcnow()
    events = icalevents.parse_events(content, start=now, end=now)
    for event in events:
        # fix timezone for all-day events
        if not event.start.tzinfo:
            log.info(
                f"Using calendar default timezone {cal_tz} for {_event_repr(event)}"
            )
            event.start = event.start.replace(tzinfo=cal_tz)
        if not event.end.tzinfo:
            event.end = event.end.replace(tzinfo=cal_tz)
    return events
