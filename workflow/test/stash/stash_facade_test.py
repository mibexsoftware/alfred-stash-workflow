# -*- coding: utf-8 -*-

from unittest import TestCase

import freezegun
import httpretty
from src.stash.project import Project
from src.stash.pull_request import PullRequest
from src.stash.pull_request_suggestion import PullRequestSuggestion
from src.stash.repository import Repository
from src.stash.stash_facade import StashFacade


class TestStashFacade(TestCase):
    def setUp(self):
        self.stash_facade = StashFacade(stash_host='http://localhost:7990/stash')

    @httpretty.activate
    def test_get_all_projects(self):
        # GIVEN
        self._mock_projects_rest_call()
        # WHEN
        projects = self.stash_facade.all_projects()
        # THEN
        self.assertEquals(
            [Project(key='PRJ',
                     name='My Cool Project',
                     description='The description for my cool project.',
                     link='http://link/to/project')],
            projects
        )

    @httpretty.activate
    def test_get_all_repositories(self):
        # GIVEN
        self._mock_repos_rest_call()
        # WHEN
        repositories = self.stash_facade.all_repositories()
        # THEN
        self.assertEquals([Repository(name='My repo 1', slug='my-repo1', link='http://link/to/repository1',
                                      project_key='PRJ', project_name='My Cool Project', public=False, fork=False,
                                      clone_url='https://<baseURL>/scm/PRJ/my-repo1.git'),
                           Repository(name='My repo 2', slug='my-repo2', link='http://link/to/repository2',
                                      project_key='PRJ', project_name='My Cool Project', public=True, fork=True,
                                      clone_url='https://<baseURL>/scm/PRJ/my-repo2.git')],
                          repositories)

    @httpretty.activate
    def test_my_pull_requests_to_review(self):
        # GIVEN
        self._mock_pull_requests_rest_call()
        # WHEN
        pull_requests = self.stash_facade.my_pull_requests_to_review()
        # THEN
        self.assertEquals(
            [PullRequest(pull_request_id=1,
                         from_branch='dev',
                         to_branch='master',
                         title='Dev',
                         link='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1',
                         repo_name='rep_1',
                         project_key='PROJECT_1')],
            pull_requests
        )

    @httpretty.activate
    def test_my_created_pull_requests(self):
        # GIVEN
        self._mock_pull_requests_rest_call()
        # WHEN
        pull_requests = self.stash_facade.my_created_pull_requests()
        # THEN
        self.assertEquals(
            [PullRequest(pull_request_id=1,
                         from_branch='dev',
                         to_branch='master',
                         title='Dev',
                         link='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1',
                         repo_name='rep_1',
                         project_key='PROJECT_1')],
            pull_requests
        )

    @httpretty.activate
    def test_open_pull_requests(self):
        # GIVEN
        self._mock_repos_rest_call()
        self._mock_open_pull_requests_rest_call()
        # WHEN
        pull_requests = self.stash_facade.open_pull_requests()
        # THEN
        self.assertEquals(
            [PullRequest(pull_request_id=1,
                         from_branch='dev',
                         to_branch='master',
                         title='Dev',
                         link='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1',
                         repo_name='rep_1',
                         project_key='PROJECT_1'),
             PullRequest(pull_request_id=1,
                         from_branch='dev',
                         to_branch='master',
                         title='Dev',
                         link='http://localhost:7990/stash/projects/PROJECT_1/repos/rep_2/pull-requests/1',
                         repo_name='rep_2',
                         project_key='PROJECT_1')],
            pull_requests
        )

    @httpretty.activate
    def test_pull_request_suggestions(self):
        # GIVEN
        self._mock_pull_request_suggestions_rest_call()
        # WHEN
        suggestions = self.stash_facade.my_pull_request_suggestions()
        # THEN
        self.assertEquals(
            PullRequestSuggestion(change_time=1478187004000,
                                  repo_slug='alfred-stash-workflow',
                                  repo_name='Alfred Stash Workflow',
                                  project_name='Mira',
                                  project_key='MIRA',
                                  project_url='https://localhost:7990/bitbucket/projects/MIRA',
                                  ref_id='refs/heads/master',
                                  display_id='master'),
            suggestions[0]
        )

    def _mock_pull_request_suggestions_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/stash/rest/api/1.0/dashboard/pull-request-suggestions",
                               body='''{
                                          "size": 1,
                                          "limit": 3,
                                          "isLastPage": true,
                                          "values": [
                                            {
                                              "changeTime": 1478187004000,
                                              "refChange": {
                                                "ref": {
                                                  "id": "refs/heads/master",
                                                  "displayId": "master",
                                                  "type": "BRANCH"
                                                },
                                                "refId": "refs/heads/master",
                                                "fromHash": "f9431d41a78f766138220f73a3b50286766df770",
                                                "toHash": "41bf84305faa3a5882f1eeb19a3298098f574bf9",
                                                "type": "UPDATE"
                                              },
                                              "repository": {
                                                "slug": "alfred-stash-workflow",
                                                "id": 352,
                                                "name": "Alfred Stash Workflow",
                                                "scmId": "git",
                                                "state": "AVAILABLE",
                                                "statusMessage": "Available",
                                                "forkable": false,
                                                "project": {
                                                  "key": "MIRA",
                                                  "id": 41,
                                                  "name": "Mira",
                                                  "description": "Our phantastic Atlassian plug-ins",
                                                  "public": false,
                                                  "type": "NORMAL",
                                                  "links": {
                                                    "self": [
                                                      {
                                                        "href": "https://localhost:7990/bitbucket/projects/MIRA"
                                                      }
                                                    ]
                                                  }
                                                },
                                                "public": false,
                                                "links": {
                                                  "clone": [
                                                    {
                                                      "href": "https://mrueegg@localhost:7990/bitbucket/scm/mira/alfred-stash-workflow.git",
                                                      "name": "http"
                                                    },
                                                    {
                                                      "href": "ssh://git@localhost:8442/mira/alfred-stash-workflow.git",
                                                      "name": "ssh"
                                                    }
                                                  ],
                                                  "self": [
                                                    {
                                                      "href": "https://localhost:7990/bitbucket/projects/MIRA/repos/alfred-stash-workflow/browse"
                                                    }
                                                  ]
                                                }
                                              },
                                              "fromRef": {
                                                "id": "refs/heads/master",
                                                "displayId": "master",
                                                "type": "BRANCH"
                                              },
                                              "toRef": {
                                                "id": "refs/heads/master",
                                                "displayId": "master",
                                                "type": "BRANCH"
                                              }
                                            }
                                          ],
                                          "start": 0
                                        }''',
                               content_type="application/json")

    def _mock_pull_requests_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/stash/rest/api/1.0/inbox/pull-requests",
                               body='''{
                                          "size": 1,
                                          "limit": 25,
                                          "isLastPage": true,
                                          "values": [
                                            {
                                              "id": 1,
                                              "version": 0,
                                              "title": "Dev",
                                              "description": "* a couple of changes",
                                              "state": "OPEN",
                                              "open": true,
                                              "closed": false,
                                              "createdDate": 1436283154855,
                                              "updatedDate": 1436283154855,
                                              "fromRef": {
                                                "id": "refs/heads/dev",
                                                "displayId": "dev",
                                                "latestChangeset": "bf97bf79c6d2b14757d6a929a576a65be296cc20",
                                                "repository": {
                                                  "slug": "rep_1",
                                                  "id": 11,
                                                  "name": "rep_1",
                                                  "scmId": "git",
                                                  "state": "AVAILABLE",
                                                  "statusMessage": "Available",
                                                  "forkable": true,
                                                  "project": {
                                                    "key": "PROJECT_1",
                                                    "id": 1,
                                                    "name": "Project 1",
                                                    "description": "Default configuration project #1",
                                                    "public": false,
                                                    "type": "NORMAL",
                                                    "link": {
                                                      "url": "/projects/PROJECT_1",
                                                      "rel": "self"
                                                    },
                                                    "links": {
                                                      "self": [
                                                        {
                                                          "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                        }
                                                      ]
                                                    }
                                                  },
                                                  "public": false,
                                                  "link": {
                                                    "url": "/projects/PROJECT_1/repos/rep_1/browse",
                                                    "rel": "self"
                                                  },
                                                  "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                  "links": {
                                                    "clone": [
                                                      {
                                                        "href": "ssh://git@localhost:7999/project_1/rep_1.git",
                                                        "name": "ssh"
                                                      },
                                                      {
                                                        "href": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                        "name": "http"
                                                      }
                                                    ],
                                                    "self": [
                                                      {
                                                        "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                      }
                                                    ]
                                                  }
                                                }
                                              },
                                              "toRef": {
                                                "id": "refs/heads/master",
                                                "displayId": "master",
                                                "latestChangeset": "0c38f167ab09ceb7d9ec1bb3d41ff3993a34d803",
                                                "repository": {
                                                  "slug": "rep_1",
                                                  "id": 11,
                                                  "name": "rep_1",
                                                  "scmId": "git",
                                                  "state": "AVAILABLE",
                                                  "statusMessage": "Available",
                                                  "forkable": true,
                                                  "project": {
                                                    "key": "PROJECT_1",
                                                    "id": 1,
                                                    "name": "Project 1",
                                                    "description": "Default configuration project #1",
                                                    "public": false,
                                                    "type": "NORMAL",
                                                    "link": {
                                                      "url": "/projects/PROJECT_1",
                                                      "rel": "self"
                                                    },
                                                    "links": {
                                                      "self": [
                                                        {
                                                          "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                        }
                                                      ]
                                                    }
                                                  },
                                                  "public": false,
                                                  "link": {
                                                    "url": "/projects/PROJECT_1/repos/rep_1/browse",
                                                    "rel": "self"
                                                  },
                                                  "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                  "links": {
                                                    "clone": [
                                                      {
                                                        "href": "ssh://git@localhost:7999/project_1/rep_1.git",
                                                        "name": "ssh"
                                                      },
                                                      {
                                                        "href": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                        "name": "http"
                                                      }
                                                    ],
                                                    "self": [
                                                      {
                                                        "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                      }
                                                    ]
                                                  }
                                                }
                                              },
                                              "locked": false,
                                              "author": {
                                                "user": {
                                                  "name": "admin",
                                                  "emailAddress": "admin@example.com",
                                                  "id": 1,
                                                  "displayName": "Administrator",
                                                  "active": true,
                                                  "slug": "admin",
                                                  "type": "NORMAL",
                                                  "link": {
                                                    "url": "/users/admin",
                                                    "rel": "self"
                                                  },
                                                  "links": {
                                                    "self": [
                                                      {
                                                        "href": "http://localhost:7990/stash/users/admin"
                                                      }
                                                    ]
                                                  }
                                                },
                                                "role": "AUTHOR",
                                                "approved": false
                                              },
                                              "reviewers": [],
                                              "participants": [],
                                              "attributes": {
                                                "resolvedTaskCount": [
                                                  "0"
                                                ],
                                                "commentCount": [
                                                  "5"
                                                ],
                                                "openTaskCount": [
                                                  "0"
                                                ]
                                              },
                                              "link": {
                                                "url": "/projects/PROJECT_1/repos/rep_1/pull-requests/1",
                                                "rel": "self"
                                              },
                                              "links": {
                                                "self": [
                                                  {
                                                    "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1"
                                                  }
                                                ]
                                              }
                                            }
                                          ],
                                          "start": 0
                                        }''',
                               content_type="application/json")

    def _mock_open_pull_requests_rest_call(self):
        httpretty.register_uri(httpretty.GET,
                               "http://localhost:7990/stash/rest/api/1.0/projects/PRJ/repos/my-repo1/pull-requests?limit=100",
                               body='''{
                                                                 "size": 1,
                                                                 "limit": 25,
                                                                 "isLastPage": true,
                                                                 "values": [
                                                                   {
                                                                     "id": 1,
                                                                     "version": 0,
                                                                     "title": "Dev",
                                                                     "description": "* a couple of changes",
                                                                     "state": "OPEN",
                                                                     "open": true,
                                                                     "closed": false,
                                                                     "createdDate": 1436283154855,
                                                                     "updatedDate": 1436283154855,
                                                                     "fromRef": {
                                                                       "id": "refs/heads/dev",
                                                                       "displayId": "dev",
                                                                       "latestChangeset": "bf97bf79c6d2b14757d6a929a576a65be296cc20",
                                                                       "repository": {
                                                                         "slug": "rep_1",
                                                                         "id": 11,
                                                                         "name": "rep_1",
                                                                         "scmId": "git",
                                                                         "state": "AVAILABLE",
                                                                         "statusMessage": "Available",
                                                                         "forkable": true,
                                                                         "project": {
                                                                           "key": "PROJECT_1",
                                                                           "id": 1,
                                                                           "name": "Project 1",
                                                                           "description": "Default configuration project #1",
                                                                           "public": false,
                                                                           "type": "NORMAL",
                                                                           "link": {
                                                                             "url": "/projects/PROJECT_1",
                                                                             "rel": "self"
                                                                           },
                                                                           "links": {
                                                                             "self": [
                                                                               {
                                                                                 "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                                               }
                                                                             ]
                                                                           }
                                                                         },
                                                                         "public": false,
                                                                         "link": {
                                                                           "url": "/projects/PROJECT_1/repos/rep_1/browse",
                                                                           "rel": "self"
                                                                         },
                                                                         "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                                         "links": {
                                                                           "clone": [
                                                                             {
                                                                               "href": "ssh://git@localhost:7999/project_1/rep_1.git",
                                                                               "name": "ssh"
                                                                             },
                                                                             {
                                                                               "href": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                                               "name": "http"
                                                                             }
                                                                           ],
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                                             }
                                                                           ]
                                                                         }
                                                                       }
                                                                     },
                                                                     "toRef": {
                                                                       "id": "refs/heads/master",
                                                                       "displayId": "master",
                                                                       "latestChangeset": "0c38f167ab09ceb7d9ec1bb3d41ff3993a34d803",
                                                                       "repository": {
                                                                         "slug": "rep_1",
                                                                         "id": 11,
                                                                         "name": "rep_1",
                                                                         "scmId": "git",
                                                                         "state": "AVAILABLE",
                                                                         "statusMessage": "Available",
                                                                         "forkable": true,
                                                                         "project": {
                                                                           "key": "PROJECT_1",
                                                                           "id": 1,
                                                                           "name": "Project 1",
                                                                           "description": "Default configuration project #1",
                                                                           "public": false,
                                                                           "type": "NORMAL",
                                                                           "link": {
                                                                             "url": "/projects/PROJECT_1",
                                                                             "rel": "self"
                                                                           },
                                                                           "links": {
                                                                             "self": [
                                                                               {
                                                                                 "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                                               }
                                                                             ]
                                                                           }
                                                                         },
                                                                         "public": false,
                                                                         "link": {
                                                                           "url": "/projects/PROJECT_1/repos/rep_1/browse",
                                                                           "rel": "self"
                                                                         },
                                                                         "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                                         "links": {
                                                                           "clone": [
                                                                             {
                                                                               "href": "ssh://git@localhost:7999/project_1/rep_1.git",
                                                                               "name": "ssh"
                                                                             },
                                                                             {
                                                                               "href": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                                               "name": "http"
                                                                             }
                                                                           ],
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                                             }
                                                                           ]
                                                                         }
                                                                       }
                                                                     },
                                                                     "locked": false,
                                                                     "author": {
                                                                       "user": {
                                                                         "name": "admin",
                                                                         "emailAddress": "admin@example.com",
                                                                         "id": 1,
                                                                         "displayName": "Administrator",
                                                                         "active": true,
                                                                         "slug": "admin",
                                                                         "type": "NORMAL",
                                                                         "link": {
                                                                           "url": "/users/admin",
                                                                           "rel": "self"
                                                                         },
                                                                         "links": {
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/users/admin"
                                                                             }
                                                                           ]
                                                                         }
                                                                       },
                                                                       "role": "AUTHOR",
                                                                       "approved": false
                                                                     },
                                                                     "reviewers": [],
                                                                     "participants": [],
                                                                     "attributes": {
                                                                       "resolvedTaskCount": [
                                                                         "0"
                                                                       ],
                                                                       "commentCount": [
                                                                         "5"
                                                                       ],
                                                                       "openTaskCount": [
                                                                         "0"
                                                                       ]
                                                                     },
                                                                     "link": {
                                                                       "url": "/projects/PROJECT_1/repos/rep_1/pull-requests/1",
                                                                       "rel": "self"
                                                                     },
                                                                     "links": {
                                                                       "self": [
                                                                         {
                                                                           "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/pull-requests/1"
                                                                         }
                                                                       ]
                                                                     }
                                                                   }
                                                                 ],
                                                                 "start": 0
                                                               }''',
                               content_type="application/json")
        httpretty.register_uri(httpretty.GET,
                               "http://localhost:7990/stash/rest/api/1.0/projects/PRJ/repos/my-repo2/pull-requests?limit=100",
                               body='''{
                                                                 "size": 1,
                                                                 "limit": 25,
                                                                 "isLastPage": true,
                                                                 "values": [
                                                                   {
                                                                     "id": 1,
                                                                     "version": 0,
                                                                     "title": "Dev",
                                                                     "description": "* a couple of changes",
                                                                     "state": "OPEN",
                                                                     "open": true,
                                                                     "closed": false,
                                                                     "createdDate": 1436283154855,
                                                                     "updatedDate": 1436283154855,
                                                                     "fromRef": {
                                                                       "id": "refs/heads/dev",
                                                                       "displayId": "dev",
                                                                       "latestChangeset": "bf97bf79c6d2b14757d6a929a576a65be296cc20",
                                                                       "repository": {
                                                                         "slug": "rep_2",
                                                                         "id": 11,
                                                                         "name": "rep_2",
                                                                         "scmId": "git",
                                                                         "state": "AVAILABLE",
                                                                         "statusMessage": "Available",
                                                                         "forkable": true,
                                                                         "project": {
                                                                           "key": "PROJECT_1",
                                                                           "id": 1,
                                                                           "name": "Project 1",
                                                                           "description": "Default configuration project #1",
                                                                           "public": false,
                                                                           "type": "NORMAL",
                                                                           "link": {
                                                                             "url": "/projects/PROJECT_1",
                                                                             "rel": "self"
                                                                           },
                                                                           "links": {
                                                                             "self": [
                                                                               {
                                                                                 "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                                               }
                                                                             ]
                                                                           }
                                                                         },
                                                                         "public": false,
                                                                         "link": {
                                                                           "url": "/projects/PROJECT_1/repos/rep_2/browse",
                                                                           "rel": "self"
                                                                         },
                                                                         "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_2.git",
                                                                         "links": {
                                                                           "clone": [
                                                                             {
                                                                               "href": "ssh://git@localhost:7999/project_1/rep_2.git",
                                                                               "name": "ssh"
                                                                             },
                                                                             {
                                                                               "href": "http://admin@localhost:7990/stash/scm/project_1/rep_2.git",
                                                                               "name": "http"
                                                                             }
                                                                           ],
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                                             }
                                                                           ]
                                                                         }
                                                                       }
                                                                     },
                                                                     "toRef": {
                                                                       "id": "refs/heads/master",
                                                                       "displayId": "master",
                                                                       "latestChangeset": "0c38f167ab09ceb7d9ec1bb3d41ff3993a34d803",
                                                                       "repository": {
                                                                         "slug": "rep_1",
                                                                         "id": 11,
                                                                         "name": "rep_1",
                                                                         "scmId": "git",
                                                                         "state": "AVAILABLE",
                                                                         "statusMessage": "Available",
                                                                         "forkable": true,
                                                                         "project": {
                                                                           "key": "PROJECT_1",
                                                                           "id": 1,
                                                                           "name": "Project 1",
                                                                           "description": "Default configuration project #1",
                                                                           "public": false,
                                                                           "type": "NORMAL",
                                                                           "link": {
                                                                             "url": "/projects/PROJECT_1",
                                                                             "rel": "self"
                                                                           },
                                                                           "links": {
                                                                             "self": [
                                                                               {
                                                                                 "href": "http://localhost:7990/stash/projects/PROJECT_1"
                                                                               }
                                                                             ]
                                                                           }
                                                                         },
                                                                         "public": false,
                                                                         "link": {
                                                                           "url": "/projects/PROJECT_1/repos/rep_2/browse",
                                                                           "rel": "self"
                                                                         },
                                                                         "cloneUrl": "http://admin@localhost:7990/stash/scm/project_1/rep_2.git",
                                                                         "links": {
                                                                           "clone": [
                                                                             {
                                                                               "href": "ssh://git@localhost:7999/project_1/rep_2.git",
                                                                               "name": "ssh"
                                                                             },
                                                                             {
                                                                               "href": "http://admin@localhost:7990/stash/scm/project_1/rep_1.git",
                                                                               "name": "http"
                                                                             }
                                                                           ],
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_1/browse"
                                                                             }
                                                                           ]
                                                                         }
                                                                       }
                                                                     },
                                                                     "locked": false,
                                                                     "author": {
                                                                       "user": {
                                                                         "name": "admin",
                                                                         "emailAddress": "admin@example.com",
                                                                         "id": 1,
                                                                         "displayName": "Administrator",
                                                                         "active": true,
                                                                         "slug": "admin",
                                                                         "type": "NORMAL",
                                                                         "link": {
                                                                           "url": "/users/admin",
                                                                           "rel": "self"
                                                                         },
                                                                         "links": {
                                                                           "self": [
                                                                             {
                                                                               "href": "http://localhost:7990/stash/users/admin"
                                                                             }
                                                                           ]
                                                                         }
                                                                       },
                                                                       "role": "AUTHOR",
                                                                       "approved": false
                                                                     },
                                                                     "reviewers": [],
                                                                     "participants": [],
                                                                     "attributes": {
                                                                       "resolvedTaskCount": [
                                                                         "0"
                                                                       ],
                                                                       "commentCount": [
                                                                         "5"
                                                                       ],
                                                                       "openTaskCount": [
                                                                         "0"
                                                                       ]
                                                                     },
                                                                     "link": {
                                                                       "url": "/projects/PROJECT_1/repos/rep_2/pull-requests/1",
                                                                       "rel": "self"
                                                                     },
                                                                     "links": {
                                                                       "self": [
                                                                         {
                                                                           "href": "http://localhost:7990/stash/projects/PROJECT_1/repos/rep_2/pull-requests/1"
                                                                         }
                                                                       ]
                                                                     }
                                                                   }
                                                                 ],
                                                                 "start": 0
                                                               }''',
                               content_type="application/json")

    def _mock_projects_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/stash/rest/api/1.0/projects",
                               body='''{
                                            "size": 1,
                                            "limit": 25,
                                            "isLastPage": true,
                                            "values": [
                                                {
                                                    "key": "PRJ",
                                                    "id": 1,
                                                    "name": "My Cool Project",
                                                    "description": "The description for my cool project.",
                                                    "public": true,
                                                    "type": "NORMAL",
                                                    "link": {
                                                        "url": "http://link/to/project",
                                                        "rel": "self"
                                                    },
                                                    "links": {
                                                        "self": [
                                                            {
                                                                "href": "http://link/to/project"
                                                            }
                                                        ]
                                                    }
                                                }
                                            ],
                                            "start": 0
                                        }''',
                               content_type="application/json")

    def _mock_repos_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/stash/rest/api/1.0/repos",
                               responses=[
                                   httpretty.Response(body='''{
                                            "size": 1,
                                            "limit": 1,
                                            "isLastPage": false,
                                            "values": [
                                                {
                                                    "slug": "my-repo1",
                                                    "id": 1,
                                                    "name": "My repo 1",
                                                    "scmId": "git",
                                                    "state": "AVAILABLE",
                                                    "statusMessage": "Available",
                                                    "forkable": true,
                                                    "project": {
                                                        "key": "PRJ",
                                                        "id": 1,
                                                        "name": "My Cool Project",
                                                        "description": "The description for my cool project.",
                                                        "public": true,
                                                        "type": "NORMAL",
                                                        "link": {
                                                            "url": "http://link/to/project",
                                                            "rel": "self"
                                                        },
                                                        "links": {
                                                            "self": [
                                                                {
                                                                    "href": "http://link/to/project"
                                                                }
                                                            ]
                                                        }
                                                    },
                                                    "public": false,
                                                    "cloneUrl": "https://<baseURL>/scm/PRJ/my-repo1.git",
                                                    "link": {
                                                        "url": "http://link/to/repository",
                                                        "rel": "self"
                                                    },
                                                    "links": {
                                                        "clone": [
                                                            {
                                                                "href": "https://<baseURL>/scm/PRJ/my-repo1.git",
                                                                "name": "http"
                                                            },
                                                            {
                                                                "href": "ssh://git@<baseURL>/PRJ/my-repo.git",
                                                                "name": "ssh"
                                                            }
                                                        ],
                                                        "self": [
                                                            {
                                                                "href": "http://link/to/repository1",
                                                                "rel": "self"
                                                            }
                                                        ]
                                                    }
                                                }
                                            ],
                                            "start": 0,
                                            "nextPageStart": 1
                                        }'''),
                                   httpretty.Response(body='''{
                                            "size": 1,
                                            "limit": 1,
                                            "isLastPage": true,
                                            "values": [
                                                {
                                                    "slug": "my-repo2",
                                                    "id": 1,
                                                    "name": "My repo 2",
                                                    "scmId": "git",
                                                    "state": "AVAILABLE",
                                                    "statusMessage": "Available",
                                                    "forkable": true,
                                                    "origin": {
                                                        "slug": "my-repo",
                                                        "id": 1,
                                                        "name": "My repo",
                                                        "scmId": "git",
                                                        "state": "AVAILABLE",
                                                        "statusMessage": "Available",
                                                        "forkable": true,
                                                        "project": {
                                                            "key": "PRJ",
                                                            "id": 1,
                                                            "name": "My Cool Project",
                                                            "description": "The description for my cool project.",
                                                            "public": true,
                                                            "type": "NORMAL",
                                                            "link": {
                                                                "url": "http://link/to/project",
                                                                "rel": "self"
                                                            },
                                                            "links": {
                                                                "self": [
                                                                    {
                                                                        "href": "http://link/to/project"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    },
                                                    "project": {
                                                        "key": "PRJ",
                                                        "id": 1,
                                                        "name": "My Cool Project",
                                                        "description": "The description for my cool project.",
                                                        "public": true,
                                                        "type": "NORMAL",
                                                        "link": {
                                                            "url": "http://link/to/project",
                                                            "rel": "self"
                                                        },
                                                        "links": {
                                                            "self": [
                                                                {
                                                                    "href": "http://link/to/project"
                                                                }
                                                            ]
                                                        }
                                                    },
                                                    "public": true,
                                                    "cloneUrl": "https://<baseURL>/scm/PRJ/my-repo2.git",
                                                    "link": {
                                                        "url": "http://link/to/repository",
                                                        "rel": "self"
                                                    },
                                                    "links": {
                                                        "clone": [
                                                            {
                                                                "href": "https://<baseURL>/scm/PRJ/my-repo2.git",
                                                                "name": "http"
                                                            },
                                                            {
                                                                "href": "ssh://git@<baseURL>/PRJ/my-repo.git",
                                                                "name": "ssh"
                                                            }
                                                        ],
                                                        "self": [
                                                            {
                                                                "href": "http://link/to/repository2",
                                                                "rel": "self"
                                                            }
                                                        ]
                                                    }
                                                }
                                            ],
                                            "start": 1
                                        }''')
                               ],
                               content_type="application/json")
