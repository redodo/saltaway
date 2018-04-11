# -*- coding: utf-8 -*-


class SaltawayException(Exception):
    """The root Saltaway exception class to be easily catchable"""


class RepositoryFailure(SaltawayException):
    """Raised when the implementation of the archive repository appears
    to have been changed.
    """
    def __init__(self, repository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository


class ArchivalFailure(SaltawayException):
    """Raised when the URL could not be archived"""
