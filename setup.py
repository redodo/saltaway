# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='saltaway',
    version='0.1.0',
    description='Trigger archival at verious archivers',
    url='https://github.com/redodo/saltaway',
    author='Hidde Bultsma',
    author_email='me@redodo.io',
    license='MIT',
    packages=['saltaway'],
    install_requires=[
        'lxml',
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        saltaway=saltaway.cli:cli
    '''
)
