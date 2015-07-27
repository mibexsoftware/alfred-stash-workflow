# -*- coding: utf-8 -*-

from unittest import TestCase, skip

from mock import patch, PropertyMock, ANY, call
from src.stash import PullRequest
from src.lib.workflow import Workflow
from src.actions.stash_pull_requests import PullRequestWorkflow
from test.actions import AnyStringWith


class TestStashPullRequests(TestCase):
    PULL_REQUESTS = [PullRequest(pull_request_id=1,
                                 title='Super important new feature',
                                 from_branch='develop',
                                 to_branch='master',
                                 link='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1',
                                 repo_name='repo_1',
                                 project_key='PROJECT_1'),
                     PullRequest(pull_request_id=4,
                                 title='Nasty bug',
                                 from_branch='bugfix/XYZ',
                                 to_branch='develop',
                                 link='http://localhost:7990/stash/projects/PROJECT_2/repos/rep_2/pull-requests/3',
                                 repo_name='repo_2',
                                 project_key='PROJECT_2')]

    def tearDown(self):
        # clear caches
        wf = Workflow()
        wf.clear_cache()

    @patch('src.lib.workflow.Workflow')
    def test_with_two_pull_requests_from_cache_no_query_should_add_both_to_alfred_list(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PULL_REQUESTS
        workflow.cached_data_fresh.return_value = True

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        two_calls = [call(title=u'repo_1 #1: develop → master',
                          largetext='Super important new feature',
                          subtitle='Super important new feature',
                          valid=True,
                          icon=ANY,
                          arg='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1'),
                     call(title=u'repo_2 #4: bugfix/XYZ → develop',
                          largetext='Nasty bug',
                          subtitle='Nasty bug',
                          valid=True,
                          icon=ANY,
                          arg='http://localhost:7990/stash/projects/PROJECT_2/repos/rep_2/pull-requests/3')]
        workflow.add_item.assert_has_calls(two_calls)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_pull_requests_from_cache_query_only_one_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PULL_REQUESTS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['Super'])
        workflow.filter.return_value = [self.PULL_REQUESTS[0]]

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        workflow.add_item.assert_called_once_with(title=u'repo_1 #1: develop → master',
                                                  largetext='Super important new feature',
                                                  subtitle='Super important new feature',
                                                  valid=True,
                                                  icon=ANY,
                                                  arg='http://localhost:7990/stash/projects/'
                                                      'PROJECT_1/repos/rep_1/pull-requests/1')
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_pull_request_from_cache_query_none_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PULL_REQUESTS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['XXX'])
        workflow.filter.return_value = []

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        workflow.add_item.assert_called_once_with('No matching pull requests found.', icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @skip("Skip this test temporarily until it is clear what causes them to fail now and then")
    @patch('src.lib.workflow.background')
    @patch('src.lib.workflow.Workflow')
    def test_get_pull_requests_from_stash_should_yield_refresh_message(self, workflow, background):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data_fresh.return_value = False
        background.is_running.return_value = True

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        workflow.add_item.assert_called_once_with('Getting data from Stash. Please try again in a second or two...',
                                                  valid=False, icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_notify_when_update_available(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=True)

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        workflow.add_item.assert_called_once_with(AnyStringWith('is available'),
                                                  'Use `workflow:update` to install',
                                                  icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_fail_when_stash_host_is_not_set(self, workflow):
        # GIVEN
        type(workflow).settings = PropertyMock(return_value={})
        type(workflow).args = PropertyMock(return_value=['--review'])

        # WHEN
        wf = PullRequestWorkflow(wf=workflow, cache_key=None, update_interval=None)
        wf.run()

        # THEN
        workflow.add_item.assert_called_once_with('Stash host URL not set. Type `stash config host <host_url>`.',
                                                  valid=False,
                                                  icon=ANY)
        self.assertTrue(workflow.send_feedback.called)
