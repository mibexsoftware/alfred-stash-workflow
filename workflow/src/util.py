# -*- coding: utf-8 -*-
import subprocess

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
    subprocess.call(['/usr/bin/env', 'osascript', 'launcher/launch_alfred.scpt', args])
