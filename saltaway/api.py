# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, as_completed

from .repositories import ArchiveIs, InternetArchive


REPOSITORIES = (
    ArchiveIs,
    InternetArchive,
)


MAX_WORKERS = min(len(REPOSITORIES), 4)


def push(url, repos=REPOSITORIES, max_age=0):
    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        future_to_repo = {
            executor.submit(repo().push, url, max_age=max_age): repo
            for repo in repos
        }
        for future in as_completed(future_to_repo):
            yield future_to_repo[future], future.result()


def pull(url, repos=REPOSITORIES):
    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        future_to_repo = {
            executor.submit(repo().pull, url): repo
            for repo in repos
        }
        for future in as_completed(future_to_repo):
            try:
                yield [future_to_repo[future]].extend(future.result())
            except NotImplementedError:
                pass
