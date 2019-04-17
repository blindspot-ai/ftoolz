#!/usr/bin/env python

from os.path import exists
from setuptools import find_packages, setup
from setuptools.dist import Distribution

from ftoolz import __version__ as ftoolz_version


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self) -> bool:
        return True


ftoolz_requirements = [
    'cytoolz==0.9.0.1',
    'cytoolz-stubs==0.0.1',
]

dev_requirements = [
    'bumpversion==0.5.3',
    'twine==1.13.0',
]

test_requirements = [
    # 'astroid==2.2.5',
    'astroid==2.1.0',
    'coverage==4.5.1',
    'flake8==3.7.7',
    # 'mypy==0.700',
    'mypy==0.630',
    'nose==1.3.7',
    # 'pylint==2.3.0',
    'pylint==2.2.0',
    'typed-ast==1.1.1',
]

setup(
    name='ftoolz',
    version=ftoolz_version,
    license='MIT',
    description='Collection of higher-order and utility functions',
    long_description=(open('README.md').read() if exists('README.md') else ''),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/blindspot-ai/ftoolz',
    maintainer='Martin Matyasek',
    maintainer_email='martin.matyasek@blindspot.ai',
    keywords='functional utility cytoolz itertools functools',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    distclass=BinaryDistribution,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=ftoolz_requirements,
    extras_require={'dev': dev_requirements, 'test': test_requirements},
    test_suite='tests',
    tests_require=ftoolz_requirements + test_requirements,
)
