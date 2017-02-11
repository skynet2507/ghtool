import os
from subprocess import call

from setuptools import Command, find_packages, setup

from ghtool import __version__


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        print "ghtool test invoked..."

    def finalize_options(self):
        print "ghtool test finished."

    def run(self):
        errno = call(['py.test', '--cov=ghtool', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='ghtool',
    version=__version__,
    description='A gihub CLI in python',
    url='https://github.com/filip/ghtool',
    author='Filip Tomic',
    author_email='skynet.ft@hotmail.com',
    license='UNLICENSE',
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['docopt', 'requests', 'grequests'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'ghtool=ghtool.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
