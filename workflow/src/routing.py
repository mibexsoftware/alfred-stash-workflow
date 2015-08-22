# -*- coding: utf-8 -*-
from src import icons, __version__
from src.actions import HOST_URL
from src.actions.configure import ConfigureWorkflowAction
from src.actions.help import HelpWorkflowAction
from src.actions.index import IndexWorkflowAction
from src.actions.projects import ProjectWorkflowAction
from src.actions.pull_requests import PullRequestWorkflowAction
from src.actions.repositories import RepositoryWorkflowAction
from src.util import workflow, call_alfred

WORKFLOW_ACTIONS = {
    ':config':       ConfigureWorkflowAction,
    ':projects':     ProjectWorkflowAction,
    ':repos':        RepositoryWorkflowAction,
    ':pullrequests': PullRequestWorkflowAction,
    ':help':         HelpWorkflowAction
}

def route(args):  # e.g., args = ":config sethost http://localhost,--exec"
    command_string = args[0]  # :config sethost http://localhost
    command = command_string.split(' ')

    if not workflow().settings.get(HOST_URL, None) and 'sethost' not in command:
        call_alfred('stash:config sethost ')
        return

    handler = IndexWorkflowAction
    action = next(iter(command), None)
    if action:
        handler = WORKFLOW_ACTIONS.get(action, IndexWorkflowAction)

    if '--exec' in args:
        handler().execute(command, cmd_pressed='--cmd' in args, shift_pressed='--shift' in args)
    else:  # show menu
        handler().menu(command)
        _notify_if_upgrade_available()
        workflow().send_feedback()


def _notify_if_upgrade_available():
    if workflow().update_available:
        new_version = workflow().cached_data('__workflow_update_status', max_age=0)['version']
        workflow().add_item('An update is available!',
                            'Update the workflow from version {} to {}'.format(__version__, new_version),
                            arg=':config update',
                            valid=True,
                            icon=icons.UPDATE)
