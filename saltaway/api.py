# -*- coding: utf-8 -*-
from .repositories import ArchiveIs, WaybackMachine


def push(url, repos=[ArchiveIs, WaybackMachine]):
    if not isinstance(repos, (list, tuple)):
        repos = [repos]
    for repo in repos:
        yield repo.name, repo().push(url)
