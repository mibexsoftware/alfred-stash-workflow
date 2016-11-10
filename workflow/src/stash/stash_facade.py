# -*- coding: utf-8 -*-

from src.lib import requests


# We use requests library for HTTP connections because workflow.web does not verify SSL certificates!
# see http://www.deanishe.net/alfred-workflow/api/web.html
from distutils.version import StrictVersion

from src.stash.project import Project
from src.stash.pull_request import PullRequest
from src.stash.pull_request_suggestion import PullRequestSuggestion
from src.stash.repository import Repository


class StashFacade(object):
    STASH_API_VERSION = '1.0'
    INBOX_PLUGIN_API_VERSION = '1.0'

    def __init__(self, stash_host, stash_user=None, stash_pw=None, verify=True):
        super(StashFacade, self).__init__()
        self._stash_user = stash_user
        self._stash_pw = stash_pw
        self._verify = verify
        if stash_host.endswith("/"):
            self._base_url = stash_host[:-1]
        else:
            self._base_url = stash_host
        self._stash_api_base = '{}/rest/api/{}'.format(self._base_url, self.STASH_API_VERSION)
        self._stash_inbox_plugin_api_base = '{}/rest/inbox/{}'.format(self._base_url, self.INBOX_PLUGIN_API_VERSION)
        self._bbs_inbox_plugin_api_base = '{}/rest/api/{}/inbox'.format(self._base_url, self.INBOX_PLUGIN_API_VERSION)

    def application_version(self):
        response = self._get(self._stash_url('/application-properties'), params={}).json()
        return StrictVersion(response['version'])

    def all_projects(self):
        return [Project.from_json(json)
                for json in self._page(self._stash_url('/projects'), params={'limit': 100})]

    def all_repositories(self):
        all_repos = [Repository.from_json(json) for json in
                     self._page(self._stash_url('/repos'), params={'limit': 1000})]
        return sorted(all_repos, key=lambda r: r.project_key)

    def open_pull_requests(self):
        return [PullRequest.from_json(json)
                for repo in self.all_repositories()
                for json in self._page(self._stash_url('/projects/{}/repos/{}/pull-requests').format(repo.project_key,
                                                                                                     repo.slug),
                                       params={'limit': 100})]

    def project_avatar(self, project_key):
        response = self._get(self._stash_url('/projects/{}/avatar.png'.format(project_key)), params={}, stream=True)
        response.raw.decode_content = True
        return response.raw

    def user_avatar(self, user_slug):
        response = self._get(self._stash_url('/users/{}'.format(user_slug.lower())), params={'avatarSize': 64}).json()
        if 'avatarUrl' not in response:
            return None
        if response['avatarUrl'].startswith(('https://', 'http://')):  # external gravatar
            avatar_url = response['avatarUrl']
        else:  # internal Stash avatar
            avatar_url = '{}/users/{}/avatar.png?s=64'.format(self._base_url, user_slug.lower())
        response = self._get(avatar_url, params={}, stream=True)
        response.raw.decode_content = True
        return response.raw

    def my_pull_requests_to_review(self, appl_version):
        return [PullRequest.from_json(json)
                for json in self._page(self._inbox_plugin_url('/pull-requests', appl_version), params={'limit': 100})]

    def my_pull_request_suggestions(self, appl_version):
        # before BBS 4.10, pull request suggestions API was not supported
        if appl_version < StrictVersion('4.10.0'):
            return []
        return [PullRequestSuggestion.from_json(json)
                for json in self._page(self._stash_url('/dashboard/pull-request-suggestions'), params={'limit': 25})]

    def my_created_pull_requests(self, appl_version):
        return [PullRequest.from_json(json)
                for json in self._page(self._inbox_plugin_url('/pull-requests', appl_version), params={'role': 'author',
                                                                                                       'limit': 100})]

    def verify_stash_connection(self):
        self._get(self._stash_url('/repos'), params={'size': 1})

    def _stash_url(self, resource_path):
        return self._url(self._stash_api_base, resource_path)

    def _inbox_plugin_url(self, resource_path, appl_version):
        inbox_base_url = self._stash_inbox_plugin_api_base if appl_version < StrictVersion('4.5.0') \
            else self._bbs_inbox_plugin_api_base
        return self._url(inbox_base_url, resource_path)

    def _url(self, api_base, resource_path):
        if not resource_path.startswith("/"):
            resource_path = "/" + resource_path
        return api_base + resource_path

    def _get(self, url, params, stream=False):
        if self._stash_user is not None:
            credentials = (self._stash_user, self._stash_pw)
        else:
            credentials = None
        options = {
            'auth': credentials,
            'verify': self._verify,
            'stream': stream
        }
        response = requests.get(url, params=params, **options)
        response.raise_for_status()
        return response

    def _page(self, url, params):
        has_more = True
        start = None

        while has_more:
            if start is not None:
                params['start'] = start

            response = self._get(url, params)
            json = response.json()

            if 'values' not in json:
                return

            for item in json['values']:
                yield item

            has_more = not json['isLastPage']
            if has_more:
                start = json['nextPageStart']
