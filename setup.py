from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
# To use a consistent encoding
from codecs import open
from os import path
import sys
import shlex

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        if isinstance(self.pytest_args, str):
            self.pytest_args = shlex.split(self.pytest_args)
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


version='0.1.3'
setup(
    name='pysrim',
    version=version,
    description='Srim Automation of Tasks',
    long_description='Pythonic Wrapper to SRIM',
    author='Christopher Ostrouchov',
    author_email='chris.ostrouchov+pysrim@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass = {'test': PyTest},
    keywords='material srim automation plotting',
    url='https://gitlab.aves.io/costrouc/pysrim',
    download_url = 'https://gitlab.aves.io/costrouc/pysrim/repository/archive.zip?ref=v%s' % version,
    packages=find_packages(exclude=['examples', 'tests']),
    package_data={
        'srim': ['data/*.yaml'],
    },
    install_requires=['pyyaml', 'numpy>=1.10.0'],
    tests_require=['pytest'],
)
