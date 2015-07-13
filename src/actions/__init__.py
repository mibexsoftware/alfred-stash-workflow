# -*- coding: utf-8 -*-


from src.lib.docopt import docopt
from src.lib.workflow import (PasswordNotFound, ICON_ERROR, Workflow, ICON_WARNING, ICON_SYNC)
from src.lib.workflow.background import run_in_background
from src.lib.workflow.background import is_running
from src.lib.workflow import ICON_INFO

from src.stash.stash_facade import StashFacade

# If the workflow throws an error, this URL will be displayed in the log
# and Alfred's debugger. It can also be opened directly in a web browser with the workflow:help
HELP_URL = 'https://github.com/mibexsoftware/alfred-stash-workflow/issues'

# How often to check for new / updated Stash data
UPDATE_INTERVAL = 6 * 60 * 60  # every six hours

PROJECT_AVATAR_DIR = 'project_avatars'

# By default, Workflow.filter() will match and return anything that contains all the characters in
# query in the same order, regardless of case. So we want to restrict this by using a min score
# see http://alfredworkflow.readthedocs.org/en/latest/user-manual/filtering.html for more information
SEARCH_MIN_SCORE = 20

HOST_URL = 'host_url'
USER_NAME = 'user_name'
USER_PW = 'user_pw'
VERIFY_CERT = 'verify_cert'

PROJECTS_CACHE_KEY = 'projects'
REPOS_CACHE_KEY = 'repos'
PULL_REQUESTS_CACHE_KEY = 'pullrequests'


def build_stash_facade(wf):
    stash_host = wf.settings.get(HOST_URL, None)
    if stash_host is None:
        raise ValueError('Stash host URL not set. Type `stash config host <host_url>`.')
    stash_user = wf.settings.get(USER_NAME, None)
    try:
        stash_pw = wf.get_password(USER_PW)
    except PasswordNotFound:
        stash_pw = None
    verify_cert = wf.settings.get(VERIFY_CERT, False)
    return StashFacade(stash_host, stash_user, stash_pw, verify_cert)


def _check_stash_config(wf):
    try:
        build_stash_facade(wf)
        return True
    except ValueError, e:
        wf.logger.error('Invalid Stash settings', e)
        wf.add_item(str(e), valid=False, icon=ICON_ERROR)
        wf.send_feedback()
        return False


def notify_if_upgrade_available(wf):
    if wf.update_available:
        v = wf.cached_data('__workflow_update_status', max_age=0)['version']
        wf.logger.info('Newer version ({}) is available'.format(v))
        wf.add_item('Version {} is available'.format(v),
                    'Use `workflow:update` to install',
                    icon=ICON_SYNC)


def _notify_if_cache_update_in_progess(wf):
    # Notify the user if the cache is being updated
    if is_running('update'):
        wf.add_item('Getting data from Stash. Please try again in a second or two...',
                    valid=False,
                    icon=ICON_INFO)


def _get_data_from_cache(wf, cache_key):
    # Get repos from cache. Set `data_func` to None, as we don't want to
    # update the cache in this script and `max_age` to 0 because we want
    # the cached data regardless of age
    data = wf.cached_data(cache_key, None, max_age=0)

    # Start update script if cached data is too old (or doesn't exist)
    if not wf.cached_data_fresh(cache_key, max_age=UPDATE_INTERVAL):
        _update_stash_cache()

    return data


def _update_stash_cache():
    cmd = ['/usr/bin/python', '-msrc.actions.update']
    run_in_background('update', cmd)


def create_workflow():
    wf = Workflow(help_url=HELP_URL,
                  update_settings={
                      'github_slug': 'mibexsoftware/alfred-stash-workflow',
                      # Optional number of days between checks for updates
                      'frequency': 7
                  })
    return wf


class StashFilteredWorkflow(object):
    def __init__(self, entity_name, wf, doc_args, cache_key):
        self.entity_name = entity_name
        self.wf = wf
        self.args = docopt(doc_args, wf.args)
        self.cache_key = cache_key

    def run(self):
        self.wf.logger.debug('workflow args: {}'.format(self.args))

        if not _check_stash_config(self.wf):
            return 0

        if self.args.get('--update'):
            _update_stash_cache()

        notify_if_upgrade_available(self.wf)
        entities = _get_data_from_cache(self.wf, self.cache_key)
        _notify_if_cache_update_in_progess(self.wf)
        query = self.args.get('<query>')

        if query and entities:  # query may not be empty or contain only whitespace. This will raise a ValueError.
            entities = self.wf.filter(query, entities, key=self.get_result_filter(), min_score=SEARCH_MIN_SCORE)
            self.wf.logger.debug('{} {} matching `{}`'.format(self.entity_name, len(entities), query))

        if not entities:
            self.wf.add_item('No matching {} found.'.format(self.entity_name), icon=ICON_WARNING)
            self.wf.send_feedback()
            return 0

        for e in entities:
            self.add_to_result_list(e, self.wf)

        self.wf.send_feedback()
        return 0

    def get_result_filter(self):
        raise NotImplementedError

    def add_to_result_list(self, entity, wf):
        raise NotImplementedError
