#!/usr/bin/env python3
import logging
import datetime

#import ical
from ical.calendar_stream import IcsCalendarStream

import zoneinfo

#import icalendar
import requests
#from icalevents import icalevents

# imports needed for vendored _get_cal_tz:
#from dateutil.tz import gettz
#from pytz import timezone

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
    if event.computed_duration.days >= 1:
        start = str(event.start)
        return f"{event.summary} {start}"
    else:
        if str(event.end.date()) == str(event.start.date()):
            return f"{event.summary} {event.start.strftime('%Y-%m-%d %H:%M %Z')} to {event.end.strftime('%H:%M %Z')}"
        else:
            return f"{event.summary} {event.start.strftime('%Y-%m-%d %H:%M %Z')} to {event.end.strftime('%Y-%m-%d %H:%M %Z')}"


def _get_cal_tz(calendar):
    """
    Get the calendar timezone

    This code is extracted from icalevents.icalparser
    It's not in an importable form over there, so copy it outright

    License: MIT
    """
    # if there's exactly one TZ in the calendar, assume it's the
    # right one to use
    if len(calendar.timezones) == 1:
        return zoneinfo.ZoneInfo(calendar.timezones[0].tz_id)
    # ...otherwise return UTC
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
            calendar = IcsCalendarStream.calendar_from_ics(f.read())
    elif "://" not in url:
        path = url
        with open(path) as f:
            calendar = IcsCalendarStream.calendar_from_ics(f.read())
    else:
        r = requests.get(url)
        r.raise_for_status()
        calendar = IcsCalendarStream.calendar_from_ics(r.text)

    cal_tz = _get_cal_tz(calendar)
    #print(cal_tz)
    #now = utcnow()
    now = datetime.datetime(2023, 3, 2, 20, 0, 0, 0, tzinfo=cal_tz)
    #events = icalevents.parse_events(content, start=now, end=now)
    events = calendar.timeline.at_instant(now)
    # for event in events:
        # # fix timezone for all-day events
        # if not event.dtstart.tzinfo:
        #     log.info(
        #         f"Using calendar default timezone {cal_tz} for {_event_repr(event)}"
        #     )
        #     new_start = datetime.datetime(event.dtstart.year, event.dtstart.month, event.dtstart.day, tzinfo=cal_tz)
        # if not event.dtend.tzinfo:
        #     event.dtend = cal_tz
    return events
