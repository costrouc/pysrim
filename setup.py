from setuptools import setup, find_packages

setup(
    name='srim',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'srim': ['data/*.txt']
    },
    description='Srim Automation of Tasks',
    long_description='Pythonic Wrapper to SRIM (LONG)',
    author='Christopher Ostrouchov',
    author_email='chris.ostrouchov+srim@gmail.com',
    url='https://github.com/costrouc/srim-python',
    download_url='https://github.com/costrouc/srim-python/tarball/master',
    keywords=['srim', 'automation', 'plotting'],
    setup_requires=['pytest-runner'],
    install_requires=['pyyaml'],
    tests_require=['pytest', 'pytest-mock'],
    # scripts=['scripts/']       
)
