# -*- coding: utf-8 -*-
from src import icons, HELP_URL, __version__
from src.actions import StashWorkflowAction
from src.util import workflow


class HelpWorkflowAction(StashWorkflowAction):

    def menu(self, args):
        workflow().add_item(
            'About this version',
            'Current version: {}. See here for the changelog.'.format(__version__),
            arg=':help version', valid=True, icon=icons.WHATSNEW
        )
        workflow().add_item(
            'Found a bug or miss a feature?',
            'Go through our issue database or create a new issue.',
            arg=':help issues', valid=True, icon=icons.ISSUES
        )
        workflow().add_item(
            'About us',
            'We are Mibex Software. Find out more about us.',
            arg=':help about', valid=True, icon=icons.INFO
        )
        workflow().add_item(
            'Credits',
            'Dean Jackson: Python Alfred Workflow, Ian Paterson: inspiration for a menu-based Alfred workflow.',
            arg=':help credits', valid=False, icon=icons.CREDITS
        )
        workflow().add_item('Main menu', autocomplete='', icon=icons.GO_BACK)

    def execute(self, args, cmd_pressed, shift_pressed):
        import webbrowser
        if 'version' in args:
            webbrowser.open('https://github.com/mibexsoftware/alfred-stash-workflow/releases/tag/{}'
                            .format(__version__))
        elif 'issues' in args:
            webbrowser.open(HELP_URL)
        elif 'about' in args:
            webbrowser.open('https://www.mibexsoftware.com')
