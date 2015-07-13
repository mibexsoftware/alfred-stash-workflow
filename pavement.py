# -*- coding: utf-8 -*-

from paver.easy import options, task, needs, sh, Bunch
from paver.setuputils import install_distutils_tasks
from paver.virtual import virtualenv

install_distutils_tasks()

options(
    setup=dict(
        name="Alfred-Stash-Workflow",
        packages=['src'],
        version="1.0.0",
        url="https://mibexsoftware.com",
        author="Mibex Software GmbH",
        author_email="support@mibexsoftware.com",
        license="MIT"
    ),
    virtualenv=Bunch(
        packages_to_install=['httpretty', 'wheel', 'virtualenv', 'flake8', 'nosexcover', 'nose', 'mock'],
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
    return sh('flake8 test src/actions src/stash pavement.py')


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
    sh("nosetests -d -v test")


@task
@virtualenv(dir="venv")
def coverage():
    """Runs all tests under the test/ folder structure with code coverage."""
    sh("nosetests -d  -v --with-xunit --xunit-file=tests.xml --with-xcoverage --cover-package=src test")
