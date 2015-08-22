# -*- coding: utf-8 -*-
from src import icons
from src.actions import StashWorkflowAction
from src.util import workflow


class IndexWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        workflow().add_item(
            'Search for Stash projects',
            'Search for projects and open the project page in your default browser',
            autocomplete=':projects ',
            icon=icons.PROJECTS
        )
        workflow().add_item(
            'Search for Stash repositories',
            'Search for repositories and open the repository browse page in your default browser',
            autocomplete=':repos ',
            icon=icons.REPOSITORIES
        )
        workflow().add_item(
            'Search for Stash pull requests',
            'Search in all pull requests, only the ones to review or the ones you created',
            autocomplete=':pullrequests ',
            icon=icons.PULLREQUESTS
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
