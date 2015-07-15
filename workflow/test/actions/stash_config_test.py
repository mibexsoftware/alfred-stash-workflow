# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import PropertyMock, patch, ANY
from src.actions import HOST_URL, USER_NAME, USER_PW, VERIFY_CERT
from src.lib.requests.exceptions import SSLError
from src.lib.workflow import Workflow
from src.actions.stash_config import main
from src.lib import requests

class TestStashConfig(TestCase):
    def tearDown(self):
        # clear caches
        wf = Workflow()
        wf.clear_cache()

    @patch('src.lib.workflow.Workflow')
    def test_delcache_should_invalidate_cache(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--delcache'])
        # WHEN
        main(workflow)
        # THEN
        self.assertTrue(workflow.clear_cache.called)

    @patch('src.stash.stash_facade.StashFacade.verify_stash_connection')
    @patch('src.lib.workflow.Workflow')
    def test_configcheck_should_yield_alfred_error_when_ssl_error(self, workflow, verify_stash_connection):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--check'])
        verify_stash_connection.side_effect = SSLError
        # WHEN
        main(workflow)
        # THEN
        workflow.add_item.assert_called_once_with(
            'SSL error: Try without cert verification: "stash config verifycert false".',
            icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.stash.stash_facade.StashFacade.verify_stash_connection')
    @patch('src.lib.workflow.Workflow')
    def test_configcheck_should_yield_alfred_error_when_connection_error(self, workflow, verify_stash_connection):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--check'])
        verify_stash_connection.side_effect = requests.exceptions.Timeout('Timeout')
        # WHEN
        main(workflow)
        # THEN
        workflow.add_item.assert_called_once_with('Error when connecting Stash server: Timeout', icon=ANY)
        self.assertTrue(workflow.send_feedback.called)

    @patch('src.lib.workflow.Workflow')
    def test_set_host_should_save_it_in_workflow_settings(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--sethost', 'http://localhost:7990/stash'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        self.assertEquals(workflow.settings, {HOST_URL: 'http://localhost:7990/stash'})

    @patch('src.lib.workflow.Workflow')
    def test_set_user_should_save_it_in_workflow_settings(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--setuser', 'michael'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        self.assertEquals(workflow.settings, {USER_NAME: 'michael'})

    @patch('src.lib.workflow.Workflow')
    def test_set_password_should_save_it_in_keychain(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--setpassword', 'XYZ123'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        workflow.save_password.assert_called_once_with(USER_PW, 'XYZ123')

    @patch('src.lib.workflow.Workflow')
    def test_enable_certcheck_should_save_it_in_workflow_settings(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--setverify', 'true'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        self.assertEquals(workflow.settings, {VERIFY_CERT: True})

    @patch('src.lib.workflow.Workflow')
    def test_disable_certcheck_should_save_it_in_workflow_settings(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--setverify', 'false'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        self.assertEquals(workflow.settings, {VERIFY_CERT: False})

    @patch('src.lib.workflow.Workflow')
    def test_invalid_certcheck_value_should_be_ignored(self, workflow):
        # GIVEN
        type(workflow).args = PropertyMock(return_value=['--setverify', 'FF'])
        type(workflow).settings = PropertyMock(return_value={})
        # WHEN
        main(workflow)
        # THEN
        self.assertEquals(workflow.settings, {})
