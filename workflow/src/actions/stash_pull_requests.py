#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stash_pull_requests.py [options] [<query>]

Alfred action to query pull requests to review for the calling user.

Usage:
    stash_pull_requests.py [--review|--created|--open] [<query>]
    stash_pull_requests.py --update

Options:
    --review        Search for pull requests to review of the current suer
    --created       Search for created pull requests of the current user
    --open          Search for all open pull requests
    --update        Update cache
    -h, --help      Show this message

"""

from __future__ import print_function, unicode_literals

import sys

from src.actions import PROJECT_AVATAR_DIR, create_workflow, StashFilteredWorkflow, \
    PULL_REQUESTS_REVIEW_CACHE_KEY, PULL_REQUESTS_CREATED_CACHE_KEY, PULL_REQUESTS_OPEN_CACHE_KEY, \
    UPDATE_INTERVALL_MY_PULL_REQUESTS, UPDATE_INTERVALL_OPEN_PULL_REQUESTS
from src.lib.docopt import docopt


class PullRequestWorkflow(StashFilteredWorkflow):
    def __init__(self, wf, cache_key, update_interval):
        super(PullRequestWorkflow, self).__init__(entity_name='pull requests',
                                                  wf=wf,
                                                  doc_args=__doc__,
                                                  cache_key=cache_key,
                                                  update_interval=update_interval)

    def _add_to_result_list(self, pull_request, wf):
        wf.add_item(title=u'{} #{}: {} → {}'.format(pull_request.repo_name, pull_request.pull_request_id,
                                                    pull_request.from_branch, pull_request.to_branch),
                    subtitle=pull_request.title,
                    arg=pull_request.link,
                    largetext=pull_request.title,
                    valid=True,
                    icon=wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, pull_request.project_key)))

    def _get_result_filter(self):
        return lambda pr: u' '.join([pr.repo_name, pr.title])


def main(wf):
    args = docopt(__doc__)
    cache_key = None
    update_interval = None
    if args.get('--review'):
        cache_key = PULL_REQUESTS_REVIEW_CACHE_KEY
        update_interval = UPDATE_INTERVALL_MY_PULL_REQUESTS
    elif args.get('--created'):
        cache_key = PULL_REQUESTS_CREATED_CACHE_KEY
        update_interval = UPDATE_INTERVALL_MY_PULL_REQUESTS
    elif args.get('--open'):
        cache_key = PULL_REQUESTS_OPEN_CACHE_KEY
        update_interval = UPDATE_INTERVALL_OPEN_PULL_REQUESTS
    pull_request_workflow = PullRequestWorkflow(wf=wf,
                                                cache_key=cache_key,
                                                update_interval=update_interval)
    return pull_request_workflow.run()


if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
