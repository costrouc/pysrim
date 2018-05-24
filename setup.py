# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pysrim',
    version='0.5.7',
    description='Srim Automation of Tasks via Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/costrouc/pysrim',
    author='Christopher Ostrouchov',
    author_email='chris.ostrouchov+pysrim@gmail.com',
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='material srim automation plotting',
    download_url='https://gitlab.com/costrouc/pysrim/repository/master/archive.zip',
    packages=find_packages(exclude=['examples', 'tests', 'test_files', 'docs']),
    package_data={
        'srim': ['data/*.yaml'],
    },
    setup_requires=['pytest-runner', 'setuptools>=38.6.0'],  # >38.6.0 needed for markdown README.md
    install_requires=['pyyaml', 'numpy>=1.10.0'],
    tests_require=['pytest', 'pytest-mock', 'pytest-cov'],
)
