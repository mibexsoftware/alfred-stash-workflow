# -*- coding: utf-8 -*-

from unittest import TestCase, skip

from mock import patch, PropertyMock, ANY, call
from src.stash import Repository
from src.lib.workflow import Workflow
from src.actions.stash_repos import main, PUBLIC, FORK
from test.actions import AnyStringWith


class TestStashRepos(TestCase):
    REPOS = [Repository(name='My repo 1', slug='rep_1', link='http://link/to/repository1', project_key='PRJ',
                        project_name='My Cool Project', public=False, fork=False,
                        clone_url="https://<baseURL>/scm/PRJ/my-repo1.git"),
             Repository(name='My repo 2', slug='rep_2', link='http://link/to/repository2', project_key='PRJ',
                        project_name='My Cool Project', public=True, fork=True,
                        clone_url='https://<baseURL>/scm/PRJ/my-repo2.git')]

    def tearDown(self):
        # clear caches
        wf = Workflow()
        wf.clear_cache()

    @patch('src.lib.workflow.Workflow')
    def test_with_two_repositories_from_cache_no_query_should_add_both_to_alfred_list(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.REPOS
        workflow.cached_data_fresh.return_value = True

        # WHEN
        main(workflow)

        # THEN
        two_calls = [call(title='My Cool Project / My repo 1  ',
                          copytext='https://<baseURL>/scm/PRJ/my-repo1.git',
                          valid=True, icon=ANY, arg='http://link/to/repository1'),
                     call(title=u'My Cool Project / My repo 2 {} {}'.format(PUBLIC, FORK),
                          copytext='https://<baseURL>/scm/PRJ/my-repo2.git',
                          valid=True, icon=ANY, arg='http://link/to/repository2')]
        workflow.add_item.assert_has_calls(two_calls)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_repositories_from_cache_query_only_one_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.REPOS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['repo 1'])
        workflow.filter.return_value = [self.REPOS[0]]

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with(title='My Cool Project / My repo 1  ',
                                                  copytext='https://<baseURL>/scm/PRJ/my-repo1.git',
                                                  valid=True, icon=ANY, arg='http://link/to/repository1')
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_repositories_from_cache_query_none_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.REPOS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['XXX'])
        workflow.filter.return_value = []

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with('No matching repositories found.', icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @skip("Skip this test temporarily until it is clear what causes them to fail now and then")
    @patch('src.lib.workflow.background')
    @patch('src.lib.workflow.Workflow')
    def test_get_repositories_from_stash_should_yield_refresh_message(self, workflow, background):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data_fresh.return_value = False
        background.is_running.return_value = True

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with('Getting data from Stash. Please try again in a second or two...',
                                                  valid=False, icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_notify_when_update_available(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=True)

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with(AnyStringWith('is available'),
                                                  'Use `workflow:update` to install',
                                                  icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_fail_when_stash_host_is_not_set(self, workflow):
        # GIVEN
        type(workflow).settings = PropertyMock(return_value={})

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with('Stash host URL not set. Type `stash config host <host_url>`.',
                                                  valid=False,
                                                  icon=ANY)
        self.assertTrue(workflow.send_feedback.called)
