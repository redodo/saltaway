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
        'lxml>=4.0',
        'click>=5.1',
        'requests>=2.0',
        'pendulum>=1.3',
    ],
    extras_require={
        'dev': [
            'pytest>=3',
            'coverage',
            'tox',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'saltaway = saltaway.cli:cli',
        ],
    },
)
