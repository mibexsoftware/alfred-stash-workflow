#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stash_repos.py [options] [<query>]

Alfred action to query Stash repositories.

Usage:
    stash_repos.py [<query>]
    stash_repos.py --update

Options:
    --update        Update cache
    -h, --help      Show this message

"""

from __future__ import print_function, unicode_literals

import sys

from src.actions import PROJECT_AVATAR_DIR, create_workflow, StashFilteredWorkflow, REPOS_CACHE_KEY

# Icons shown in Alfred results
FORK = '⑂'
PUBLIC = '🔓'


class RepositoryWorkflow(StashFilteredWorkflow):
    def __init__(self, wf):
        super(RepositoryWorkflow, self).__init__(entity_name='repositories',
                                                 wf=wf,
                                                 doc_args=__doc__,
                                                 cache_key=REPOS_CACHE_KEY)

    def add_to_result_list(self, repo, wf):
        wf.add_item(title='{} / {} {} {}'.format(repo.project_name,
                                                 repo.name,
                                                 PUBLIC if repo.public else '',
                                                 FORK if repo.fork else ''),
                    arg=repo.link,
                    valid=True,
                    copytext=repo.clone_url,  # allows to use CMD+C to copy the clone URL
                    icon=wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, repo.project_key)))

    def get_result_filter(self):
        return lambda r: u' '.join([r.name, r.project_name])


def main(wf):
    repository_workflow = RepositoryWorkflow(wf=wf)
    return repository_workflow.run()


if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
