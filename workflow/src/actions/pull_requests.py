# -*- coding: utf-8 -*-
from src import icons
from src.actions import StashWorkflowAction, StashFilterableMenu, PROJECT_AVATAR_DIR, PULL_REQUESTS_OPEN_CACHE_KEY, \
    UPDATE_INTERVAL_OPEN_PULL_REQUESTS, UPDATE_INTERVAL_MY_PULL_REQUESTS, UPDATE_INTERVAL_CREATED_PULL_REQUESTS, \
    PULL_REQUESTS_REVIEW_CACHE_KEY, PULL_REQUESTS_CREATED_CACHE_KEY, PULL_REQUEST_SUGGESTIONS_CACHE_KEY, \
    UPDATE_INTERVAL_PULL_REQUEST_SUGGESTIONS, get_data_from_cache
from src.util import workflow, call_alfred


class PullRequestFilterableMenu(StashFilterableMenu):
    def __init__(self, args, update_interval, cache_key):
        super(PullRequestFilterableMenu, self).__init__(entity_name='pull requests',
                                                        update_interval=update_interval,
                                                        cache_key=cache_key,
                                                        args=args)

    def _add_to_result_list(self, pull_request):
        workflow().add_item(title=unicode(pull_request),
                            subtitle=pull_request.title,
                            arg=':pullrequests ' + pull_request.link,
                            largetext=pull_request.title,
                            valid=True,
                            icon=workflow().cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, pull_request.project_key)))

    def _get_result_filter(self):
        return lambda pr: u' '.join([pr.repo_name, pr.title])

    def _add_item_after_last_result(self):
        workflow().add_item(
            'Back',
            autocomplete=':pullrequests ', icon=icons.GO_BACK
        )


_counters = {
    0:  u'',
    1:  u'①',
    2:  u'②',
    3:  u'③',
    4:  u'④',
    5:  u'⑤',
    6:  u'⑥',
    7:  u'⑦',
    8:  u'⑧',
    9:  u'⑨',
    10: u'⑩',
    11: u'⑪',
    12: u'⑫',
    13: u'⑬',
    14: u'⑭',
    15: u'⑮',
    16: u'⑯',
    17: u'⑰',
    18: u'⑱',
    19: u'⑲',
    20: u'⑳'
}


_pull_request_modes = {
    'open':    (PULL_REQUESTS_OPEN_CACHE_KEY, UPDATE_INTERVAL_OPEN_PULL_REQUESTS),
    'review':  (PULL_REQUESTS_REVIEW_CACHE_KEY, UPDATE_INTERVAL_MY_PULL_REQUESTS),
    'created': (PULL_REQUESTS_CREATED_CACHE_KEY, UPDATE_INTERVAL_CREATED_PULL_REQUESTS),
    'suggestions': (PULL_REQUEST_SUGGESTIONS_CACHE_KEY, UPDATE_INTERVAL_PULL_REQUEST_SUGGESTIONS)
}


def _num_pull_requests(mode):
    cache_key, update_interval = _pull_request_modes[mode]
    data = get_data_from_cache(cache_key, update_interval)
    return _counters.get(len(data), u'⑳⁺') if data else ''


class PullRequestWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        if len(args) == 2:
            workflow().add_item(
                u'Suggested pull requests {}'.format(_num_pull_requests('suggestions')),
                'Suggested pull requests to raise based on your recent commits',
                arg=':pullrequests suggestions',
                icon=icons.PR_SUGGESTIONS,
                valid=True
            )
            workflow().add_item(
                u'All open pull requests {}'.format(_num_pull_requests('open')),
                'Search in all open pull requests',
                arg=':pullrequests open',
                icon=icons.OPEN,
                valid=True
            )
            workflow().add_item(
                u'Your pull requests to review {}'.format(_num_pull_requests('review')),
                'Search in pull requests you have to review',
                arg=':pullrequests review',
                icon=icons.REVIEW,
                valid=True
            )
            workflow().add_item(
                u'Your created pull requests {}'.format(_num_pull_requests('created')),
                'Search in pull requests you created',
                arg=':pullrequests created',
                icon=icons.CREATED,
                valid=True
            )
            workflow().add_item(
                'Main menu',
                autocomplete='', icon=icons.GO_BACK
            )
        else:
            cache_key, update_interval = _pull_request_modes[args[-2]]
            pull_request_menu = PullRequestFilterableMenu(args, update_interval, cache_key)
            return pull_request_menu.run()

    def execute(self, args, cmd_pressed, shift_pressed):
        if args[-1] in _pull_request_modes.keys():
            pull_request_mode = args[-1]
            call_alfred('stash:pullrequests {} '.format(pull_request_mode))
        else:
            import webbrowser
            webbrowser.open(args[-1])
