# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime

import pytz
from src import HELP_URL, __version__
from src.lib.workflow import Workflow

# inspired by https://github.com/idpaterson/alfred-wunderlist-workflow
_workflow = None


def workflow():
    global _workflow
    if _workflow is None:
        _workflow = Workflow(
            help_url=HELP_URL,
            update_settings={
                'github_slug': 'mibexsoftware/alfred-stash-workflow',
                'frequency': 1,
                'version': __version__
            }
        )
    return _workflow


def call_alfred(args):
    alfred_major_version = workflow().alfred_env['version'][0]
    subprocess.call([
        '/usr/bin/env', 'osascript', '-l', 'JavaScript',
        'launcher/launch_alfred.scpt', args, alfred_major_version
    ])


def pretty_date(date, now=datetime.now()):
    diff = now - date
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return "?"

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " week(s) ago"
    if day_diff < 365:
        return str(day_diff / 30) + " month(s) ago"
    return str(day_diff / 365) + " year(s) ago"
