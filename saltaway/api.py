# -*- coding: utf-8 -*-
import concurrent.futures

from .repositories import ArchiveIs, WaybackMachine


REPOSITORIES = (
    ArchiveIs,
    WaybackMachine,
)


def push(url, repos=REPOSITORIES):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_repo = {
            executor.submit(repo().push, url): repo
            for repo in repos
        }
        for future in concurrent.futures.as_completed(future_to_repo):
            yield future_to_repo[future], future.result()
