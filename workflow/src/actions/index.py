# -*- coding: utf-8 -*-
from src import icons
from src.actions import StashWorkflowAction
from src.util import workflow


class IndexWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        workflow().add_item(
            'Search for projects',
            'Search for projects and open the project page in your default browser',
            autocomplete=':projects ',
            icon=icons.PROJECTS
        )
        workflow().add_item(
            'Search for repositories',
            'Search for repositories and open the repository page in your default browser',
            autocomplete=':repos ',
            icon=icons.REPOSITORIES
        )
        workflow().add_item(
            'Search for pull requests',
            'Search for pull requests and open them in your default browser',
            autocomplete=':pullrequests ',
            icon=icons.PULL_REQUESTS
        )
        workflow().add_item(
            'Preferences',
            'Change Stash connection settings, refresh the cache or the workflow itself',
            autocomplete=':config ',
            icon=icons.SETTINGS
        )
        workflow().add_item(
            'Help',
            'Get help about the workflow and how to get support',
            autocomplete=':help ',
            icon=icons.HELP
        )
