# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import patch, call, ANY
from src.actions import PROJECTS_CACHE_KEY, REPOS_CACHE_KEY, PULL_REQUESTS_REVIEW_CACHE_KEY, \
    PULL_REQUESTS_CREATED_CACHE_KEY, PULL_REQUESTS_OPEN_CACHE_KEY, UPDATE_INTERVALL_OPEN_PULL_REQUESTS, \
    UPDATE_INTERVALL_MY_PULL_REQUESTS, UPDATE_INTERVAL_REPOS, UPDATE_INTERVAL_PROJECTS
from src.actions.update import main


class TestUpdate(TestCase):

    @patch('src.lib.workflow.Workflow')
    def test_update_checks_if_cached_data_is_still_fresh(self, workflow):
        # GIVEN

        # WHEN
        main(workflow)

        # THEN
        two_calls = [call(PROJECTS_CACHE_KEY, ANY, max_age=UPDATE_INTERVAL_PROJECTS),
                     ANY,
                     call(REPOS_CACHE_KEY, ANY, max_age=UPDATE_INTERVAL_REPOS),
                     ANY,
                     call(PULL_REQUESTS_REVIEW_CACHE_KEY, ANY, max_age=UPDATE_INTERVALL_MY_PULL_REQUESTS),
                     ANY,
                     call(PULL_REQUESTS_CREATED_CACHE_KEY, ANY, max_age=UPDATE_INTERVALL_MY_PULL_REQUESTS),
                     ANY,
                     call(PULL_REQUESTS_OPEN_CACHE_KEY, ANY, max_age=UPDATE_INTERVALL_OPEN_PULL_REQUESTS)]
        workflow.cached_data.assert_has_calls(two_calls)