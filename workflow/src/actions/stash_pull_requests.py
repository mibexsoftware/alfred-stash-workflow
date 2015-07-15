#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stash_pull_requests.py [options] [<query>]

Alfred action to query pull requests to review for the calling user.

Usage:
    stash_pull_requests.py [<query>]
    stash_pull_requests.py --update

Options:
    --update        Update cache
    -h, --help      Show this message

"""

from __future__ import print_function, unicode_literals

import sys

from src.actions import PROJECT_AVATAR_DIR, create_workflow, StashFilteredWorkflow, PULL_REQUESTS_CACHE_KEY


class PullRequestWorkflow(StashFilteredWorkflow):
    def __init__(self, wf):
        super(PullRequestWorkflow, self).__init__(entity_name='pull requests',
                                                  wf=wf,
                                                  doc_args=__doc__,
                                                  cache_key=PULL_REQUESTS_CACHE_KEY)

    def add_to_result_list(self, pull_request, wf):
        wf.add_item(title=u'{} #{}: {} → {}'.format(pull_request.repo_name, pull_request.pull_request_id,
                                                    pull_request.from_branch, pull_request.to_branch),
                    subtitle=pull_request.title,
                    arg=pull_request.link,
                    valid=True,
                    icon=wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, pull_request.project_key)))

    def get_result_filter(self):
        return lambda pr: u' '.join([pr.repo_name, pr.title])


def main(wf):
    pull_request_workflow = PullRequestWorkflow(wf=wf)
    return pull_request_workflow.run()


if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
