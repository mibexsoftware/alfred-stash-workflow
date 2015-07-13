#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stash_config.py [options] [<host_url>] [<user_name>] [<user_pw>] [<verify_cert>]

Alfred action to configure the Stash actions.

Usage:
    stash_config.py
    stash_config.py --sethost <host_url>
    stash_config.py --setuser <user_name>
    stash_config.py --setpassword <user_pw>
    stash_config.py --setverify <verify_cert>
    stash_config.py --delcache
    stash_config.py --check

Options:
    --sethost       Sets the Stash host
    --setuser       Sets the Stash user
    --setpassword   Sets the password for the Stash user
    --setverify     Configures if certificate should be checked when using HTTPS (true|false, default: true)
    --delcache      Deletes all caches with Stash data
    --check         Checks the given Stash configuration parameters
    -h, --help      Show this message

"""

from __future__ import print_function, unicode_literals

import sys

from src.actions import VERIFY_CERT, USER_NAME, HOST_URL, USER_PW, build_stash_facade, create_workflow
from src.lib.requests.exceptions import SSLError
from src.lib.workflow import ICON_ERROR, ICON_INFO


def main(wf):
    from src.lib.docopt import docopt
    args = docopt(__doc__, wf.args)

    if not wf.args:
        print(wf.settings)
    elif args.get('--delcache'):
        wf.clear_cache()
    elif args.get('--check'):
        _try_stash_connection(wf)
    else:  # Stash connection params
        _handle_connection_params(args, wf)

    return 0


def _handle_connection_params(args, wf):
    host_url = args.get('<host_url>')
    if host_url:
        wf.settings[HOST_URL] = host_url
        wf.logger.debug('Set Stash host URL to {}.'.format(host_url))
        print(host_url)  # we want this to be shown in the notification

    user_name = args.get('<user_name>')
    if user_name:
        wf.settings[USER_NAME] = user_name
        wf.logger.debug('Set Stash username to {}.'.format(user_name))
        print(user_name)  # we want this to be shown in the notification

    user_pw = args.get('<user_pw>')
    if user_pw:
        wf.save_password(USER_PW, user_pw)
        wf.logger.debug('Set Stash password to *******.')

    verify_cert = args.get('<verify_cert>')
    if verify_cert:
        if verify_cert not in ['true', 'false']:
            print('Invalid input value {}.'.format(verify_cert))
            return
        wf.settings[VERIFY_CERT] = verify_cert == 'true'
        wf.logger.debug('Certificate verification is set to {}.'.format(verify_cert))
        print('Changed verification to "{}".'.format(verify_cert))  # we want this to be shown in the notification

    # connection settings have changed, so we clear the cache to refresh Stash data next time
    wf.clear_cache()


def _try_stash_connection(wf):
    try:
        stash_facade = build_stash_facade(wf)
        stash_facade.verify_stash_connection()
    except SSLError:
        wf.add_item('SSL error: Try without cert verification: "stash config verifycert false".', icon=ICON_ERROR)
    except Exception, e:
        wf.add_item('Error when connecting Stash server: {}'.format(str(e)), icon=ICON_ERROR)
    else:
        wf.add_item('Congratulations, connection to Stash was successful!', icon=ICON_INFO)
    finally:
        wf.send_feedback()


if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
