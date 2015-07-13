# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import patch, PropertyMock, ANY, call
from src.stash import Project
from src.lib.workflow import Workflow
from src.actions.stash_projects import main
from test.actions import AnyStringWith


class TestStashProjects(TestCase):
    PROJECTS = [Project(key='PROJECT1',
                        name='My Cool Project 1',
                        description='The description for my cool project 1.',
                        link='http://link/to/project1'),
                Project(key='PROJECT2',
                        name='My Cool Project 2',
                        description='The description for my cool project 2.',
                        link='http://link/to/project2')]

    def tearDown(self):
        # clear caches
        wf = Workflow()
        wf.clear_cache()

    @patch('src.lib.workflow.Workflow')
    def test_with_two_projects_from_cache_no_query_should_add_both_to_alfred_list(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PROJECTS
        workflow.cached_data_fresh.return_value = True

        # WHEN
        main(workflow)

        # THEN
        two_calls = [call(title='My Cool Project 1', subtitle='The description for my cool project 1.',
                          valid=True, icon=ANY, arg='http://link/to/project1'),
                     call(title=u'My Cool Project 2', subtitle='The description for my cool project 2.',
                          valid=True, icon=ANY, arg='http://link/to/project2')]
        workflow.add_item.assert_has_calls(two_calls)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_projects_from_cache_query_only_one_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PROJECTS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['project 1'])
        workflow.filter.return_value = [self.PROJECTS[0]]

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with(title='My Cool Project 1',
                                                  subtitle='The description for my cool project 1.',
                                                  valid=True, icon=ANY, arg='http://link/to/project1')
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_with_two_projects_from_cache_query_none_matches(self, workflow):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data.return_value = self.PROJECTS
        workflow.cached_data_fresh.return_value = True
        type(workflow).args = PropertyMock(return_value=['XXX'])
        workflow.filter.return_value = []

        # WHEN
        main(workflow)

        # THEN
        workflow.add_item.assert_called_once_with('No matching projects found.', icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.background.is_running')
    @patch('src.lib.workflow.Workflow')
    def test_get_projects_from_stash_should_yield_refresh_message(self, workflow, is_running):
        # GIVEN
        type(workflow).update_available = PropertyMock(return_value=False)
        workflow.cached_data_fresh.return_value = False
        is_running.return_value = False

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
