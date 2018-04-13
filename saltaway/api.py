# -*- coding: utf-8 -*-
import concurrent.futures

from .repositories import ArchiveIs, InternetArchive


REPOSITORIES = (
    ArchiveIs,
    InternetArchive,
)


def push(url, repos=REPOSITORIES):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_repo = {
            executor.submit(repo().push, url): repo
            for repo in repos
        }
        for future in concurrent.futures.as_completed(future_to_repo):
            yield future_to_repo[future], future.result()


def pull(url, repos=REPOSITORIES):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_repo = {
            executor.submit(repo().pull, url): repo
            for repo in repos
        }
        for future in concurrent.futures.as_completed(future_to_repo):
            try:
                yield (future_to_repo[future], *future.result())
            except NotImplementedError:
                pass
