# -*- coding: utf-8 -*-
from datetime import datetime
from src.stash import EqualityMixin
from src.util import pretty_date


class PullRequestSuggestion(EqualityMixin):
    def __init__(self, change_time, repo_slug, repo_name, project_name,
                 project_key, project_url, ref_id, display_id):
        self.change_time = change_time
        self.repo_name = repo_name
        self.project_name = project_name
        self.project_key = project_key
        self.branch = display_id
        self.link = '{}/repos/{}/pull-requests?create&sourceBranch={}'.format(project_url, repo_slug, ref_id)
        self.title = pretty_date(datetime.fromtimestamp(change_time / 1000))

    @classmethod
    def from_json(cls, json):
        pull_request_suggestion = cls(json['changeTime'],
                                      json['repository']['slug'],
                                      json['repository']['name'],
                                      json['repository']['project']['name'],
                                      json['repository']['project']['key'],
                                      json['repository']['project']['links']['self'][0]['href'],
                                      json['refChange']['ref']['id'],
                                      json['refChange']['ref']['displayId'])
        return pull_request_suggestion

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'Your commits to {} in {} / {}'.format(self.branch,
                                                       self.repo_name,
                                                       self.project_name)
