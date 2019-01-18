#!/usr/bin/env python
from os import path
import versioneer
import sys
if sys.version_info < (3,0):
    from io import open

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


requires = []


setup_options = dict(
    name='dockerutils',
    cmdclass=versioneer.get_cmdclass(),
    version=versioneer.get_version(),
    description='Docker Utilities/Patterns for Python Projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Resero-Labs',
    url='https://github.com/resero-labs/docker-utils.git',
    scripts=[
        'scripts/create-dock',
        'scripts/build-image',
        'scripts/destroy-dock',
        'scripts/dock',
        'scripts/dock-sync',
        'scripts/genversion',
        'scripts/ls-dock',
        'scripts/publish-image',
        'scripts/register-dock',
        'scripts/run-image',
        'scripts/run-notebook',
        'scripts/ssh-dock',
        'scripts/start-dock',
        'scripts/stop-dock',
        'scripts/transfer-image'
    ],
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'awscli',
        'boto3',
        'future'
    ],
    extras_require={
        'dev': [
            'wheel>=0.29'
        ],
        'test': [
            'pytest>=3.0',
            'pytest-cov>=2.4',
            'pylint>=1.8.1'
        ],
    },
)

setup(**setup_options)
