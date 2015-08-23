# -*- coding: utf-8 -*-

from src.actions import HOST_URL, StashFilterableMenu, StashWorkflowAction, \
    UPDATE_INTERVAL_REPOS, REPOS_CACHE_KEY, PROJECT_AVATAR_DIR
from src.util import workflow

# Icons shown in Alfred results
FORK = u'⑂'
PUBLIC = u'🔓'


class RepositoryFilterableMenu(StashFilterableMenu):
    def __init__(self, args):
        super(RepositoryFilterableMenu, self).__init__(entity_name='repositories',
                                                       update_interval=UPDATE_INTERVAL_REPOS,
                                                       cache_key=REPOS_CACHE_KEY,
                                                       args=args)

    def _add_to_result_list(self, repo):
        workflow().add_item(title=u'{} / {} {} {}'.format(repo.project_name,
                                                          repo.name,
                                                          PUBLIC if repo.public else '',
                                                          FORK if repo.fork else ''),
                            arg=':repos {}/{}'.format(repo.project_key, repo.slug),
                            valid=True,
                            largetext=repo.name,
                            copytext=repo.clone_url,  # allows to use CMD+C to copy the clone URL
                            icon=workflow().cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, repo.project_key)))

    def _get_result_filter(self):
        return lambda r: u' '.join([r.name, r.project_name])


class RepositoryWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        repos_menu = RepositoryFilterableMenu(args)
        return repos_menu.run()

    def execute(self, args, cmd_pressed, shift_pressed):
        import webbrowser
        project_key, repo_slug = args[-1].split('/')
        repo_browse_url = '{}/projects/{}/repos/{}'.format(workflow().settings.get(HOST_URL), project_key, repo_slug)
        webbrowser.open(repo_browse_url)
