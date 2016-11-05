# -*- coding: utf-8 -*-

from paver.easy import options, task, needs, sh, Bunch
from paver.setuputils import install_distutils_tasks
from paver.virtual import virtualenv
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'workflow')
WORKFLOW_DIR = '~/Dropbox/configs/Alfred/Alfred.alfredpreferences/workflows'
BUNDLE_ID = 'ch.mibex.stash.alfred-workflow'

install_distutils_tasks()

options(
    setup=dict(
        name="Alfred-Stash-Workflow",
        packages=['workflow'],
        version=open('workflow/src/version').readline(),
        url="https://mibexsoftware.com",
        author="Mibex Software GmbH",
        author_email="support@mibexsoftware.com",
        license="MIT"
    ),
    virtualenv=Bunch(
        packages_to_install=['httpretty', 'wheel', 'virtualenv', 'flake8', 'nose', 'mock', 'coveralls', 'pytz'],
        script_name='bootstrap.py',
        dest_dir='venv'
    )
)


@task
@needs(['minilib', 'generate_setup', 'paver.virtual.bootstrap'])
def once():
    """Run once when you first start using this codebase"""
    return sh('python bootstrap.py')


@task
@needs(['clean', 'paver.setuputils.develop'])
@virtualenv(dir="venv")
def build():
    """Build"""
    pass


@task
@virtualenv(dir="venv")
def lint():
    """Lint Python files"""
    return sh('flake8 workflow/test workflow/src/actions workflow/src/stash pavement.py')


@task
@needs(['clean', 'build', 'lint', 'coverage'])
@virtualenv(dir="venv")
def ci():
    """Run the continuous integration stuff"""
    pass


@task
def clean():
    """Clean up the build artifacts, test results, etc."""
    return max([sh('rm -rf ./*.zip bootstrap.py ./*.egg* build .coverage coverage.xml tests.xml setup.py test.xml'),
                sh('find . -name "*.pyc" -delete')])


@task
@virtualenv(dir="venv")
def test():
    """Runs all tests under the test/ folder structure."""
    sh("nosetests -d -v workflow/test")


@task
@virtualenv(dir="venv")
def coverage():
    """Runs all tests under the test/ folder structure with code coverage."""
    sh("nosetests -d  -v --with-coverage --cover-package=workflow/src workflow/test")


@task
@virtualenv(dir="venv")
def install_libs():
    """Install shipped workflow libs."""
    sh("pip install --target=workflow/src/lib requests==2.7.0")
    sh("pip install --target=workflow/src/lib Alfred-Workflow==1.22")


@task
@virtualenv(dir="venv")
def report_to_coveralls():
    """Report coverage to coveralls.io."""
    sh("coveralls")


@task
def link():
    """Links the workflow directory to Alfred's Dropbox workflow directory."""
    return sh('ln -s {} {}/{}'.format(PROJECT_DIR, WORKFLOW_DIR, BUNDLE_ID))


@task
def unlink():
    """Unlink from Alfred's Dropbox workflow directory."""
    return sh('rm {}/{}'.format(WORKFLOW_DIR, BUNDLE_ID))
