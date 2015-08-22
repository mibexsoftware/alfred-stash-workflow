# -*- coding: utf-8 -*-

from src.stash import EqualityMixin


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
