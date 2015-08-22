# -*- coding: utf-8 -*-
from src import icons
from src.actions import StashWorkflowAction, StashFilterableMenu, PROJECT_AVATAR_DIR, PULL_REQUESTS_OPEN_CACHE_KEY, \
    UPDATE_INTERVALL_OPEN_PULL_REQUESTS, UPDATE_INTERVALL_MY_PULL_REQUESTS, UPDATE_INTERVALL_CREATED_PULL_REQUESTS, \
    PULL_REQUESTS_REVIEW_CACHE_KEY, PULL_REQUESTS_CREATED_CACHE_KEY
from src.util import workflow, call_alfred


class PullRequestFilterableMenu(StashFilterableMenu):
    def __init__(self, args, update_interval, cache_key):
        super(PullRequestFilterableMenu, self).__init__(entity_name='pull requests',
                                                        update_interval=update_interval,
                                                        cache_key=cache_key,
                                                        args=args)

    def _add_to_result_list(self, pull_request):
        workflow().add_item(title=u'{} #{}: {} → {}'.format(pull_request.repo_name, pull_request.pull_request_id,
                                                            pull_request.from_branch, pull_request.to_branch),
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


class PullRequestWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        if len(args) == 2:
            workflow().add_item(
                'All open pull requests',
                'Search in all open pull requests and open them in your default browser',
                arg=':pullrequests open',
                icon=icons.OPEN,
                valid=True
            )
            workflow().add_item(
                'Your pull requests to review',
                'Search in pull requests you have to review and open them in your default browser',
                arg=':pullrequests review',
                icon=icons.REVIEW,
                valid=True
            )
            workflow().add_item(
                'Your created pull requests',
                'Search in pull requests you created and open them in your default browser',
                arg=':pullrequests created',
                icon=icons.CREATED,
                valid=True
            )
            workflow().add_item(
                'Main menu',
                autocomplete='', icon=icons.GO_BACK
            )
        else:
            if 'open' in args[-2]:
                update_interval = UPDATE_INTERVALL_OPEN_PULL_REQUESTS
                cache_key = PULL_REQUESTS_OPEN_CACHE_KEY
            elif 'review' in args[-2]:
                update_interval = UPDATE_INTERVALL_MY_PULL_REQUESTS
                cache_key = PULL_REQUESTS_REVIEW_CACHE_KEY
            elif 'created' in args[-2]:
                update_interval = UPDATE_INTERVALL_CREATED_PULL_REQUESTS
                cache_key = PULL_REQUESTS_CREATED_CACHE_KEY
            else:
                raise ValueError('Unknown pull request mode {}'.format(args[-2]))

            pull_request_menu = PullRequestFilterableMenu(args, update_interval, cache_key)
            return pull_request_menu.run()

    def execute(self, args, cmd_pressed, shift_pressed):
        if args[-1] in ['review', 'open', 'created']:
            pull_request_mode = args[-1]
            call_alfred('stash:pullrequests {} '.format(pull_request_mode))
        else:
            import webbrowser
            webbrowser.open(args[-1])
