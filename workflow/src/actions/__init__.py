# -*- coding: utf-8 -*-
from src import icons

from src.lib.workflow import (PasswordNotFound)
from src.lib.workflow.background import run_in_background
from src.lib.workflow.background import is_running
from src.lib.workflow import ICON_INFO
from src.lib.requests.exceptions import SSLError

from src.stash.stash_facade import StashFacade

# If the workflow throws an error, this URL will be displayed in the log
# and Alfred's debugger. It can also be opened directly in a web browser with the workflow:help
from src.util import workflow

# How often to check for new / updated Stash data
UPDATE_INTERVAL_PROJECTS = 1 * 24 * 60 * 60  # every day
UPDATE_INTERVAL_REPOS = 4 * 60 * 60  # four hours
UPDATE_INTERVAL_MY_PULL_REQUESTS = 15 * 60  # 15 minutes
UPDATE_INTERVAL_CREATED_PULL_REQUESTS = 15 * 60  # 15 minutes
UPDATE_INTERVAL_OPEN_PULL_REQUESTS = 1 * 60 * 60  # every hour

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
PULL_REQUESTS_REVIEW_CACHE_KEY = 'pullrequests'
PULL_REQUESTS_CREATED_CACHE_KEY = 'created_pullrequests'
PULL_REQUESTS_OPEN_CACHE_KEY = 'open_pullrequests'

SYNC_JOB_NAME = u'sync'


def try_stash_connection(show_success=True):
    try:
        stash_facade = build_stash_facade()
        stash_facade.verify_stash_connection()
        if show_success:
            workflow().add_item('Congratulations, connection to Stash was successful!', icon=icons.OK)
        return True
    except SSLError:
        workflow().add_item('SSL error: Try with certificate verification disabled', icon=icons.ERROR)
        return False
    except Exception, e:
        workflow().add_item('Error when connecting Stash server', str(e), icon=icons.ERROR)
        return False


def build_stash_facade():
    stash_host = workflow().settings.get(HOST_URL, None)
    if stash_host is None:
        raise ValueError('Stash host URL not set.')
    stash_user = workflow().settings.get(USER_NAME, None)
    try:
        stash_pw = workflow().get_password(USER_PW)
    except PasswordNotFound:
        stash_pw = None
    verify_cert = workflow().settings.get(VERIFY_CERT, 'false') == 'true'
    return StashFacade(stash_host, stash_user, stash_pw, verify_cert)


def _notify_if_cache_update_in_progress():
    # Notify the user if the cache is being updated
    if is_running(SYNC_JOB_NAME):
        workflow().add_item('Getting data from Stash. List will be up-to-date in a second or two...',
                            valid=False,
                            icon=icons.INFO)


class StashWorkflowAction(object):
    def menu(self, args):
        raise NotImplementedError

    def execute(self, args, cmd_pressed, shift_pressed):
        pass  # not every action can be executed


def get_data_from_cache(cache_key, update_interval):
    # Set `data_func` to None, as we don't want to update the cache in this script and `max_age` to 0
    # because we want the cached data regardless of age
    data = workflow().cached_data(cache_key, None, max_age=0)

    # Start update script if cached data is too old (or doesn't exist)
    if not workflow().cached_data_fresh(cache_key, max_age=update_interval):
        update_stash_cache()

    return data


def update_stash_cache():
    cmd = ['/usr/bin/python', '-msrc.sync']
    run_in_background(SYNC_JOB_NAME, cmd)


class StashFilterableMenu(object):
    def __init__(self, entity_name, args, update_interval, cache_key):
        self.entity_name = entity_name
        self.args = args
        self.update_interval = update_interval
        self.cache_key = cache_key

    def run(self):
        workflow().logger.debug('workflow args: {}'.format(self.args))

        data = get_data_from_cache(self.cache_key, self.update_interval)
        entities = self._transform_from_cache(data, self._get_query())
        _notify_if_cache_update_in_progress()

        query = self._get_sub_query()
        # query may not be empty or contain only whitespace. This will raise a ValueError.
        if query and entities:
            entities = workflow().filter(query, entities, key=self._get_result_filter(), min_score=SEARCH_MIN_SCORE)
            workflow().logger.debug('{} {} matching `{}`'.format(self.entity_name, len(entities), self._get_query()))

        if not entities:
            # only do a REST call in case there is no query given because only in that case it is likely that there
            # is a problem with the connection to Stash and we would like to prevent doing slow calls in here
            if query or (not query and try_stash_connection(show_success=False)):
                workflow().add_item('No matching {} found.'.format(self.entity_name), icon=icons.ERROR)
        else:
            for e in entities:
                self._add_to_result_list(e)

        self._add_item_after_last_result()

    def _get_result_filter(self):
        raise NotImplementedError

    def _transform_from_cache(self, entities, query):
        return entities

    def _get_query(self):
        return self.args[-1]

    def _get_sub_query(self):
        return self.args[-1]

    def _add_to_result_list(self, entity):
        raise NotImplementedError

    def _add_item_after_last_result(self):
        workflow().add_item(
            'Main menu',
            autocomplete='', icon=icons.GO_BACK
        )
