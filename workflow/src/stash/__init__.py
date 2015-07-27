# -*- coding: utf-8 -*-


class EqualityMixin(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Project(EqualityMixin):
    def __init__(self, key, name, description, link):
        self.key = key
        self.name = name
        self.description = description
        self.link = link

    @classmethod
    def from_json(cls, json):
        project = cls(json['key'],
                      json['name'],
                      json.get('description', ''),  # not every project has a description
                      json['links']['self'][0]['href'])
        return project

    def __str__(self):
        return 'Project(key="{}", name="{}", description="{}", link="{}")'.format(self.key,
                                                                                  self.name,
                                                                                  self.description,
                                                                                  self.link)


class Repository(EqualityMixin):
    def __init__(self, name, slug, link, project_key, project_name, public, fork, clone_url):
        self.name = name
        self.slug = slug
        self.link = link
        self.project_key = project_key
        self.project_name = project_name
        self.public = public
        self.fork = fork
        self.clone_url = clone_url

    @classmethod
    def from_json(cls, json):
        repository = cls(json['name'],
                         json['slug'],
                         json['links']['self'][0]['href'],
                         json['project']['key'],
                         json['project']['name'],
                         json['public'],
                         'origin' in json,
                         json['cloneUrl'])
        return repository

    def __str__(self):
        return ('Repository(name="{}", slug="{}", link="{}", project_key="{}", '
                'project_name="{}", public="{}", fork="{}", clone_url="{}")'
                .format(self.name, self.slug, self.link, self.project_key,
                        self.project_name, self.public, self.fork, self.clone_url))


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
