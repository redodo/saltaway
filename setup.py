# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='saltaway',
    version='0.1.1',
    description='Instantly archive web pages at various archives.',
    url='https://github.com/redodo/saltaway',
    author='Hidde Bultsma',
    author_email='me@redodo.io',
    license='MIT',
    packages=['saltaway'],
    install_requires=[
        'lxml',
        'click',
        'requests',
        'pendulum',
    ],
    entry_points='''
        [console_scripts]
        saltaway=saltaway.cli:cli
    '''
)
