#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil

import os
from src.actions import PROJECT_AVATAR_DIR, UPDATE_INTERVAL_PROJECTS, build_stash_facade, REPOS_CACHE_KEY, \
    PROJECTS_CACHE_KEY, UPDATE_INTERVAL_REPOS, UPDATE_INTERVALL_MY_PULL_REQUESTS, PULL_REQUESTS_REVIEW_CACHE_KEY, \
    PULL_REQUESTS_CREATED_CACHE_KEY, PULL_REQUESTS_OPEN_CACHE_KEY, UPDATE_INTERVALL_OPEN_PULL_REQUESTS
from src.lib.workflow import Workflow


def _my_pull_requests_to_review(wf, stash_facade):
    wf.logger.debug('Starting to fetch pull requests to review...')
    pull_requests = stash_facade.my_pull_requests_to_review()
    wf.logger.debug('Found {} pull requests to review'.format(len(pull_requests)))
    return pull_requests


def _my_created_pull_requests(wf, stash_facade):
    wf.logger.debug('Starting to fetch created pull requests...')
    pull_requests = stash_facade.my_created_pull_requests()
    wf.logger.debug('Found {} created pull requests'.format(len(pull_requests)))
    return pull_requests


def _open_pull_requests(wf, stash_facade):
    wf.logger.debug('Starting to fetch open pull requests...')
    pull_requests = stash_facade.open_pull_requests()
    wf.logger.debug('Found {} open pull requests'.format(len(pull_requests)))
    return pull_requests


def _find_all_repositories(wf, stash_facade):
    wf.logger.debug('Starting to fetch repositories...')
    repositories = stash_facade.all_repositories()
    _fetch_user_avatars(repositories, stash_facade)
    wf.logger.debug('Found {} repositories '.format(len(repositories)))
    return repositories


def _fetch_user_avatars(repositories, stash_facade):
    user_repos = set(filter(lambda r: r.project_key.startswith('~'), repositories))
    for r in user_repos:
        avatar = stash_facade.fetch_user_avatar(r.project_key[1:])
        if avatar is not None:
            with open(wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, r.project_key)), 'wb') as avatar_file:
                shutil.copyfileobj(avatar, avatar_file)


def _find_all_projects(wf, stash_facade):
    wf.logger.debug('Starting to fetch projects...')
    projects = stash_facade.all_projects()
    if not os.path.exists(wf.cachefile(PROJECT_AVATAR_DIR)):
        os.makedirs(wf.cachefile(PROJECT_AVATAR_DIR))
    for p in projects:
        avatar = stash_facade.fetch_project_avatar(p.key)
        with open(wf.cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, p.key)), 'wb') as avatar_file:
            shutil.copyfileobj(avatar, avatar_file)
    wf.logger.debug('Found {} projects '.format(len(projects)))
    return projects


def _fetch_stash_data_if_necessary(wf, stash_facade):
    # cached_data can only take a bare callable (no args),
    # so we need to wrap callables needing arguments in a function
    # that needs none.
    def wrapper_projects():
        return _find_all_projects(wf, stash_facade)

    projects = wf.cached_data(PROJECTS_CACHE_KEY, wrapper_projects, max_age=UPDATE_INTERVAL_PROJECTS)
    wf.logger.debug('{} projects cached'.format(len(projects)))

    def wrapper_repositories():
        return _find_all_repositories(wf, stash_facade)

    repos = wf.cached_data(REPOS_CACHE_KEY, wrapper_repositories, max_age=UPDATE_INTERVAL_REPOS)
    wf.logger.debug('{} repositories cached'.format(len(repos)))

    def wrapper_pull_requests_to_review():
        return _my_pull_requests_to_review(wf, stash_facade)

    pull_requests_to_review = wf.cached_data(PULL_REQUESTS_REVIEW_CACHE_KEY,
                                             wrapper_pull_requests_to_review,
                                             max_age=UPDATE_INTERVALL_MY_PULL_REQUESTS)
    wf.logger.debug('{} pull requests to review cached'.format(len(pull_requests_to_review)))

    def wrapper_created_pull_requests():
        return _my_created_pull_requests(wf, stash_facade)

    pull_requests_created = wf.cached_data(PULL_REQUESTS_CREATED_CACHE_KEY,
                                           wrapper_created_pull_requests,
                                           max_age=UPDATE_INTERVALL_MY_PULL_REQUESTS)
    wf.logger.debug('{} pull requests created cached'.format(len(pull_requests_created)))

    def wrapper_open_pull_requests():
        return _open_pull_requests(wf, stash_facade)

    open_pull_requests = wf.cached_data(PULL_REQUESTS_OPEN_CACHE_KEY,
                                        wrapper_open_pull_requests,
                                        max_age=UPDATE_INTERVALL_OPEN_PULL_REQUESTS)
    wf.logger.debug('{} open pull requests cached'.format(len(open_pull_requests)))


def main(wf):
    stash_facade = build_stash_facade(wf)
    _fetch_stash_data_if_necessary(wf, stash_facade)


if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)
