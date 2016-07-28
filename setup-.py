#!/usr/bin/env python
# encoding: utf-8
"""
setup.py -- dotfiles

::
    python setup.py --help
    python setup.py --help-commands

"""
import codecs
import logging
import os

from setuptools import setup

SETUPPY_PATH = os.path.dirname(os.path.realpath(__file__)) or '.'


def read_version_txt():
    with open(os.path.join(SETUPPY_PATH, 'VERSION.txt')) as f:
        version = next(f).strip()
    return version

VERSION = read_version_txt()
APPNAME = 'djangotestapp'

CONFIG = {}
DEBUG = CONFIG.get('debug', True)  # False # True

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-5s %(message)s')
log = logging.getLogger()

if DEBUG:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

SETUPPY_PATH = os.path.dirname(os.path.abspath(__file__)) or '.'
# log.debug('SETUPPY_PATH: %s' % SETUPPY_PATH)


def get_long_description(readme='README.rst', changelog='CHANGELOG.rst'):
    """
    Returns:
        str: README.rst and CHANGELOG.rst read into a string

    Expects README and CHANGELOG to include compatible headers
    """

    with codecs.open(os.path.join(SETUPPY_PATH, readme), 'r', 'utf8') as f:
        docs = [f.read()]
    changelog_path = os.path.join(SETUPPY_PATH, changelog)
    if os.path.exists(changelog_path):
        with codecs.open(changelog_path, 'r', 'utf8') as f:
            docs.append(f.read())
    return u'\n\n'.join(*docs)


def read_requirements_pip(path):
    import pip.req
    import pip.download
    session = pip.download.PipSession()
    return list(str(req.req)
        for req in pip.req.parse_requirements(
            path,
            session=session))


# Extra requirement sets
dev_extras = read_requirements_pip('requirements/requirements-dev.txt')
test_extras = read_requirements_pip('requirements/requirements-test.txt')
deploy_extras = read_requirements_pip('requirements/requirements-deploy.txt')
all_extras = read_requirements_pip('requirements/requirements-all.txt')

extras_require = {
    "dev": dev_extras,
    "test": test_extras,
    # "docs": docs_extras,
    "deploy": deploy_extras,
    "all": all_extras,
}


setup(
    name=APPNAME,
    version=VERSION,
    description=APPNAME,
    long_description=get_long_description(),
    keywords='{}'.format(APPNAME),
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url='https://github.com/westurner/djangotestapp',
    license='',
    packages=[
        'djangotestapp',
    ],
    #package_dir={'': ''},
    include_package_data=True,
    # package_data=package_data,
    zip_safe=False,
    # test_suite='nose.collector',
    # tests_require=testing_extras, # pip install -r requirements-testing.txt
    # install_requires=(always_install + testing_extras),
    install_requires=[],
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
