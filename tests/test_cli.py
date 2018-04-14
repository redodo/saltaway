# -*- coding: utf-8 -*-
import click
import pytest
from click.testing import CliRunner

from saltaway.cli import cli


TEST_URL = 'https://example.org'


@pytest.fixture
def runner():
    return CliRunner()


def test_push(runner):
    result_a = runner.invoke(cli, [TEST_URL, '--max-age=1h'])
    result_b = runner.invoke(cli, [TEST_URL, '--max-age=1h'])
    a_urls = result_a.output.split()
    b_urls = result_b.output.split()
    assert set(a_urls) == set(b_urls)
