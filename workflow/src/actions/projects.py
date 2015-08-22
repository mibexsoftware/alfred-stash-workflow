# -*- coding: utf-8 -*-
from src.actions import StashFilterableMenu, HOST_URL, PROJECTS_CACHE_KEY, \
    UPDATE_INTERVAL_PROJECTS, StashWorkflowAction, PROJECT_AVATAR_DIR
from src.util import workflow


class ProjectsFilterableMenu(StashFilterableMenu):
    def __init__(self, args):
        super(ProjectsFilterableMenu, self).__init__(entity_name='projects',
                                                     update_interval=UPDATE_INTERVAL_PROJECTS,
                                                     cache_key=PROJECTS_CACHE_KEY,
                                                     args=args)

    def _add_to_result_list(self, project):
        workflow().add_item(title=project.name,
                            subtitle=project.description,
                            arg=':projects {}'.format(project.key),
                            valid=True,
                            largetext=project.name,
                            icon=workflow().cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, project.key)))

    def _get_result_filter(self):
        return lambda p: u' '.join([p.name, p.description])


class ProjectWorkflowAction(StashWorkflowAction):
    def menu(self, args):
        project_workflow = ProjectsFilterableMenu(args)
        return project_workflow.run()

    def execute(self, args, cmd_pressed, shift_pressed):
        import webbrowser
        project_key = args[-1]
        project_browse_url = '{}/projects/{}'.format(workflow().settings.get(HOST_URL), project_key)
        webbrowser.open(project_browse_url)
