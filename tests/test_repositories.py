# -*- coding: utf-8 -*-
import pytest

from conftest import TEST_URL
from saltaway import ArchiveIs, InternetArchive


@pytest.fixture
def archive_is():
    return ArchiveIs()


@pytest.fixture
def internet_archive():
    return InternetArchive()


def test_archive_is_push(archive_is):
    url = archive_is.push(TEST_URL)
    assert url.startswith('http://archive.')


def test_archive_is_pull(archive_is):
    _, url = archive_is.pull(TEST_URL)
    assert url.startswith('http://archive.')


def test_internet_archive_push(internet_archive):
    url = internet_archive.push(TEST_URL)
    assert url.startswith('https://web.archive.org/web/')


def test_internet_archive_pull(internet_archive):
    _, url = internet_archive.pull(TEST_URL)
    assert url.startswith('https://web.archive.org/web/')
