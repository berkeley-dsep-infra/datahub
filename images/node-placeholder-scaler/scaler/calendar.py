#!/usr/bin/env python3
import logging
import datetime

from ical.calendar_stream import IcsCalendarStream
import requests
import zoneinfo

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
    Get the calendar timezone.

    Returns zoneinfo.ZoneInfo()
    """
    # if there's exactly one TZ in the calendar, assume it's the
    # right one to use
    if len(calendar.timezones) == 1:
        return zoneinfo.ZoneInfo(calendar.timezones[0].tz_id)
    # ...otherwise return UTC
    else:
        return zoneinfo.ZoneInfo("UTC")

def get_calendar(url: str):
    """
    Get a calendar from local file or URL.

    Returns an ical.Calendar object.
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

    if calendar:
        return calendar
    else:
        logging.error(f"Unable to get calendar from resource: {url}")

def get_events(calendar):
    """
    Get events from a calendar.

    Returns a list of currently happening ical.Event objects.
    """
    cal_tz = _get_cal_tz(calendar)
    now = datetime.datetime.now(tz=cal_tz)
    events_iter = calendar.timeline.at_instant(now)

    return [x for x in events_iter]
