#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stash_projects.py [options] [<query>]

Alfred action to query Stash projects.

Usage:
    stash_projects.py [<query>]
    stash_projects.py --update

Options:
    --update        Update cache
    -h, --help      Show this message

"""

from __future__ import print_function, unicode_literals

import sys

from src.actions import PROJECT_AVATAR_DIR, create_workflow, StashFilteredWorkflow, PROJECTS_CACHE_KEY


class ProjectFilteredWorkflow(StashFilteredWorkflow):
    def __init__(self, wf):
        super(ProjectFilteredWorkflow, self).__init__(entity_name='projects',
                                                      wf=wf,
                                                      doc_args=__doc__,
                                                      cache_key=PROJECTS_CACHE_KEY)

    def add_to_result_list(self, project, wf):
        wf.add_item(title=project.name,
                    subtitle=project.description,
                    arg=project.link,
                    valid=True,
                    icon=wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, project.key)))

    def get_result_filter(self):
        return lambda p: u' '.join([p.name, p.description])


def main(wf):
    project_workflow = ProjectFilteredWorkflow(wf=wf)
    return project_workflow.run()


if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
