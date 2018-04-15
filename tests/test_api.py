# -*- coding: utf-8 -*-
import saltaway
from conftest import TEST_URL
from saltaway.api import REPOSITORIES


def test_pull():
    result = list(saltaway.pull(TEST_URL))
    assert len(result) == len(REPOSITORIES)

    result = list(saltaway.pull(TEST_URL, repos=[saltaway.ArchiveIs]))
    assert len(result) == 1
