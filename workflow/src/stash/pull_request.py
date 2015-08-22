# -*- coding: utf-8 -*-

from src.stash import EqualityMixin


class PullRequest(EqualityMixin):
    def __init__(self, pull_request_id, from_branch, to_branch, title, link, project_key, repo_name):
        self.pull_request_id = pull_request_id
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.title = title
        self.link = link
        self.project_key = project_key
        self.repo_name = repo_name

    @classmethod
    def from_json(cls, json):
        pull_request = cls(json['id'],
                           json['fromRef']['displayId'],
                           json['toRef']['displayId'],
                           json['title'],
                           json['links']['self'][0]['href'],
                           json['fromRef']['repository']['project']['key'],
                           json['fromRef']['repository']['name'])
        return pull_request

    def __str__(self):
        return ('PullRequest(pull_request_id="{}", from_branch="{}", to_branch="{}", title="{}", '
                'link="{}", project_key="{}", repo_name="{}")'
                .format(self.pull_request_id, self.from_branch, self.to_branch, self.title,
                        self.link, self.project_key, self.repo_name))
