import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='srim',
    version='0.1',
    packages=find_packages(),
    package_data={
        'srim': ['data/*.yaml']
    },
    description='Srim Automation of Tasks',
    long_description='Pythonic Wrapper to SRIM (LONG)',
    author='Christopher Ostrouchov',
    author_email='chris.ostrouchov+srim@gmail.com',
    url='https://github.com/costrouc/srim-python',
    download_url='https://github.com/costrouc/srim-python/tarball/master',
    keywords=['srim', 'automation', 'plotting'],
    setup_requires=['pytest-runner'],
    install_requires=['pyyaml', 'numpy'],
    tests_require=['pytest>=2.7.0', 'pytest-mock'],
    cmdclass = {'test': PyTest},
    # scripts=['scripts/']       
)
