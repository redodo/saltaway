# -*- coding: utf-8 -*-
import click
import pytest
from click.testing import CliRunner

from conftest import TEST_URL
from saltaway.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_push(runner):
    result_a = runner.invoke(cli, [TEST_URL, '--max-age=1h'])
    result_b = runner.invoke(cli, [TEST_URL, '--max-age=1h'])
    a_urls = result_a.output.split()
    b_urls = result_b.output.split()
    print(result_a.output)
    print(result_b.output)
    assert set(a_urls) == set(b_urls)
