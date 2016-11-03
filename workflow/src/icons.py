# -*- coding: utf-8 -*-
from src.util import workflow

_icon_theme = None
ICON_THEME = 'icon_theme'


def alfred_is_dark():
    # copied from wunderlist workflow:
    background_rgba = workflow().alfred_env['theme_background']
    if background_rgba:
        rgb = [int(x) for x in background_rgba[5:-6].split(',')]
        return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 < 0.5
    return False


def icon_theme():
    global _icon_theme
    if not _icon_theme:
        icon_theme = workflow().settings.get(ICON_THEME)
        if icon_theme:
            _icon_theme = icon_theme
        else:
            _icon_theme = 'light' if alfred_is_dark() else 'dark'
    return _icon_theme


def icon_path(filename):
    return 'src/icons/{}/{}'.format(icon_theme(), filename)


CERT = icon_path('cert.png')
CHECK = icon_path('check.png')
ERROR = icon_path('error.png')
GO_BACK = icon_path('go_back.png')
HELP = icon_path('help.png')
HOST = icon_path('host.png')
INFO = icon_path('info.png')
ISSUES = icon_path('issues.png')
OK = icon_path('ok.png')
PASSWORD = icon_path('password.png')
PROJECTS = icon_path('projects.png')
REPOSITORIES = icon_path('repos.png')
SETTINGS = icon_path('settings.png')
PULL_REQUESTS = icon_path('pull_requests.png')
REVIEW = icon_path('review.png')
CREATED = icon_path('created.png')
OPEN = icon_path('open.png')
SYNC = icon_path('sync.png')
UPDATE = icon_path('update.png')
SWITCH_THEME = icon_path('switch_theme.png')
USER = icon_path('user.png')
WARNING = icon_path('warning.png')
WHATS_NEW = icon_path('whatsnew.png')
CREDITS = icon_path('credits.png')
