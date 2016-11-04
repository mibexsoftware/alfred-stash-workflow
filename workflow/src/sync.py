#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os

from src.actions import PROJECTS_CACHE_KEY, \
    UPDATE_INTERVAL_PROJECTS, build_stash_facade, PROJECT_AVATAR_DIR, UPDATE_INTERVAL_REPOS, REPOS_CACHE_KEY, \
    PULL_REQUESTS_REVIEW_CACHE_KEY, UPDATE_INTERVAL_MY_PULL_REQUESTS, PULL_REQUESTS_CREATED_CACHE_KEY, \
    PULL_REQUESTS_OPEN_CACHE_KEY, UPDATE_INTERVAL_OPEN_PULL_REQUESTS, PULL_REQUEST_SUGGESTIONS_CACHE_KEY, \
    UPDATE_INTERVAL_PULL_REQUEST_SUGGESTIONS, APPL_VERSION_CACHE_KEY, UPDATE_INTERVAL_APPL_VERSION
from src.lib.requests import HTTPError
from src.util import workflow


def _my_pull_requests_to_review(stash_facade, appl_version):
    workflow().logger.debug('Starting to fetch pull requests to review...')
    pull_requests = stash_facade.my_pull_requests_to_review(appl_version)
    workflow().logger.debug('Found {} pull requests to review'.format(len(pull_requests)))
    return pull_requests


def _my_created_pull_requests(stash_facade, appl_version):
    workflow().logger.debug('Starting to fetch created pull requests...')
    pull_requests = stash_facade.my_created_pull_requests(appl_version)
    workflow().logger.debug('Found {} created pull requests'.format(len(pull_requests)))
    return pull_requests


def _open_pull_requests(stash_facade):
    workflow().logger.debug('Starting to fetch open pull requests...')
    pull_requests = stash_facade.open_pull_requests()
    workflow().logger.debug('Found {} open pull requests'.format(len(pull_requests)))
    return pull_requests


def _my_pull_request_suggestions(stash_facade, appl_version):
    workflow().logger.debug('Starting to fetch pull request suggestions...')
    pull_request_suggestions = stash_facade.my_pull_request_suggestions(appl_version)
    workflow().logger.debug('Found {} pull request suggestions'.format(len(pull_request_suggestions)))
    return pull_request_suggestions


def _get_appl_version(stash_facade):
    workflow().logger.debug('Starting to get application version...')
    appl_version = stash_facade.application_version()
    workflow().logger.debug('Detected application version: {}.'.format(appl_version))
    return appl_version


def _find_all_repositories(stash_facade):
    workflow().logger.debug('Starting to fetch repositories...')
    repositories = stash_facade.all_repositories()
    _fetch_user_avatars(repositories, stash_facade)
    workflow().logger.debug('Found {} repositories '.format(len(repositories)))
    return repositories


def _fetch_user_avatars(repositories, stash_facade):
    user_repos = set(filter(lambda r: r.project_key.startswith('~'), repositories))
    for r in user_repos:
        try:
            avatar = stash_facade.user_avatar(r.project_key[1:])
            if avatar is not None:
                with open(workflow().cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, r.project_key)), 'wb') as avatar_file:
                    shutil.copyfileobj(avatar, avatar_file)
        except HTTPError:
            pass  # ignore as not every Stash user might have an avatar configured


def _find_all_projects(stash_facade):
    workflow().logger.debug('Starting to fetch projects...')
    projects = stash_facade.all_projects()
    if not os.path.exists(workflow().cachefile(PROJECT_AVATAR_DIR)):
        os.makedirs(workflow().cachefile(PROJECT_AVATAR_DIR))
    for p in projects:
        avatar = stash_facade.project_avatar(p.key)
        with open(workflow().cachefile('{}/{}'.format(PROJECT_AVATAR_DIR, p.key)), 'wb') as avatar_file:
            shutil.copyfileobj(avatar, avatar_file)
    workflow().logger.debug('Found {} projects '.format(len(projects)))
    return projects


def _fetch_stash_data_if_necessary(stash_facade):
    appl_version = workflow().cached_data(APPL_VERSION_CACHE_KEY,
                                          lambda: _get_appl_version(stash_facade),
                                          max_age=UPDATE_INTERVAL_APPL_VERSION)
    workflow().logger.debug('application version cached')

    projects = workflow().cached_data(PROJECTS_CACHE_KEY,
                                      lambda: _find_all_projects(stash_facade),
                                      max_age=UPDATE_INTERVAL_PROJECTS)
    workflow().logger.debug('{} projects cached'.format(len(projects)))

    repos = workflow().cached_data(REPOS_CACHE_KEY,
                                   lambda: _find_all_repositories(stash_facade),
                                   max_age=UPDATE_INTERVAL_REPOS)
    workflow().logger.debug('{} repositories cached'.format(len(repos)))

    pull_request_suggestions = workflow().cached_data(PULL_REQUEST_SUGGESTIONS_CACHE_KEY,
                                                      lambda: _my_pull_request_suggestions(stash_facade, appl_version),
                                                      max_age=UPDATE_INTERVAL_PULL_REQUEST_SUGGESTIONS)
    workflow().logger.debug('{} pull requests to review cached'.format(len(pull_request_suggestions)))

    pull_requests_to_review = workflow().cached_data(PULL_REQUESTS_REVIEW_CACHE_KEY,
                                                     lambda: _my_pull_requests_to_review(stash_facade, appl_version),
                                                     max_age=UPDATE_INTERVAL_MY_PULL_REQUESTS)
    workflow().logger.debug('{} pull requests to review cached'.format(len(pull_requests_to_review)))

    pull_requests_created = workflow().cached_data(PULL_REQUESTS_CREATED_CACHE_KEY,
                                                   lambda: _my_created_pull_requests(stash_facade, appl_version),
                                                   max_age=UPDATE_INTERVAL_MY_PULL_REQUESTS)
    workflow().logger.debug('{} pull requests created cached'.format(len(pull_requests_created)))

    open_pull_requests = workflow().cached_data(PULL_REQUESTS_OPEN_CACHE_KEY,
                                                lambda: _open_pull_requests(stash_facade),
                                                max_age=UPDATE_INTERVAL_OPEN_PULL_REQUESTS)
    workflow().logger.debug('{} open pull requests cached'.format(len(open_pull_requests)))


def main(wf):
    stash_facade = build_stash_facade()
    _fetch_stash_data_if_necessary(stash_facade)


if __name__ == '__main__':
    workflow().run(main)
