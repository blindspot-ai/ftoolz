#!/usr/bin/env python

from os.path import exists

from setuptools import find_packages, setup
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self) -> bool:
        return True


requirements = [
    'cytoolz==0.9.0.1',
    'cytoolz-stubs==0.0.1',
]

dev_requirements = [
    'bumpversion==0.5.3',
    'twine==3.1.0',
]

test_requirements = [
    'coverage==4.5.4',
    'flake8==3.7.9',
    'mypy==0.740',
    'nose==1.3.7',
    'pylint==2.4.4',
]


setup(
    name='ftoolz',
    version='0.4.0',
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
        'Programming Language :: Python :: 3.8',
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
    install_requires=requirements,
    extras_require={'dev': dev_requirements, 'test': test_requirements},
    test_suite='tests',
    tests_require=requirements + test_requirements,
)
