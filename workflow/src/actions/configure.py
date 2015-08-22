# -*- coding: utf-8 -*-
from src.actions import HOST_URL, USER_NAME, USER_PW, VERIFY_CERT, \
    StashWorkflowAction
from src import icons
from src.lib.workflow import PasswordNotFound
from src.util import workflow, call_alfred
from src.actions import try_stash_connection


class ConfigureWorkflowAction(StashWorkflowAction):

    def menu(self, args):
        if 'sethost' in args:
            workflow().add_item(
                'Type a new Stash host URL',
                'Enter the full URL to your Stash host, e.g. http://10.0.0.1/stash',
                valid=True, arg=' '.join(args), icon=icons.HOST
            )
            if workflow().settings.get(HOST_URL, None):
                _add_cancel_workflow_action()
        elif 'setuser' in args:
            workflow().add_item(
                'Type a new Stash username',
                'Enter the name of the Stash user which you would like to use to connect',
                valid=True, arg=' '.join(args), icon=icons.USER
            )
            _add_cancel_workflow_action()
        elif 'setpw' in args:
            workflow().add_item(
                'Type a new Stash password',
                'Enter the password of the Stash user. It will be stored encrypted in Keychain.',
                valid=True, arg=' '.join(args), icon=icons.PASSWORD
            )
            _add_cancel_workflow_action()
        elif 'check' in args:
            try_stash_connection()
            _add_cancel_workflow_action()
        else:
            workflow().add_item(
                'Stash host URL',
                workflow().settings.get(HOST_URL, 'Not configured'),
                autocomplete=':config sethost ', icon=icons.HOST
            )
            workflow().add_item(
                'Stash user name',
                workflow().settings.get(USER_NAME, 'Not configured'),
                autocomplete=':config setuser ', icon=icons.USER
            )
            try:
                pw = workflow().get_password(USER_PW)
                stash_pw = '******' if pw else 'Not configured'
            except PasswordNotFound:
                stash_pw = 'Not configured'

            workflow().add_item(
                'Stash user password',
                'Current password: {}'.format(stash_pw),
                autocomplete=':config setpw ', icon=icons.PASSWORD
            )
            verify_cert = 'Enabled' if workflow().settings.get(VERIFY_CERT, 'false') == 'true' else 'Disabled'
            workflow().add_item(
                'Validate certificate when accessing Stash over HTTPS',
                verify_cert,
                arg=':config verifycert', valid=True, icon=icons.CERT
            )
            workflow().add_item(
                'Check connection to Stash',
                'Checks if a Stash connection can be established with the given configuration.',
                autocomplete=':config check ', icon=icons.CHECK
            )
            workflow().add_item(
                'Sync Stash data cache',
                'Deletes the cache of Stash data and triggers a new synchronization in the background.',
                arg=':config sync', valid=True, icon=icons.SYNC
            )
            workflow().add_item(
                'Update workflow',
                'Updates the workflow to the latest version (will be checked automatically periodically).',
                arg=':config update', valid=True, icon=icons.UPDATE
            )
            workflow().add_item('Main menu', autocomplete='', icon=icons.GO_BACK)

    def execute(self, args, cmd_pressed, shift_pressed):
        if 'sethost' in args:
            workflow().settings[HOST_URL] = args[-1]
            print('New Stash host: {}'.format(args[-1]))
        elif 'setuser' in args:
            workflow().settings[USER_NAME] = args[-1]
            print('New Stash user: {}'.format(args[-1]))
        elif 'setpw' in args:
            workflow().save_password(USER_PW, args[-1])
            print('Saved Stash password in keychain')
        elif 'verifycert' in args:
            verify_cert = workflow().settings.get(VERIFY_CERT, 'false') == 'true'
            toggle = (str(not verify_cert)).lower()
            workflow().settings[VERIFY_CERT] = toggle
            print('Enabled certificate verification' if toggle else 'Disabled certificate verification')
        elif 'sync' in args:
            workflow().clear_cache()
            update_stash_cache()
            print('Stash data synchronization triggered')
        elif 'update' in args:
            try:
                if workflow().start_update():
                    print('Update of workflow finished')
                else:
                    print('You already have the latest workflow version')
            except Exception, e:
                print('Update of workflow failed: {}'.format(str(e)))

        call_alfred('stash:config')


def _add_cancel_workflow_action():
    workflow().add_item('Cancel', autocomplete=':config', icon=icons.GO_BACK)
