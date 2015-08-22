# -*- coding: utf-8 -*-

from src.stash import EqualityMixin


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
