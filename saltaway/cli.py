# -*- coding: utf-8 -*-
import click

import saltaway


@click.command()
@click.argument('url')
def cli(url):
    for repo_name, archive_url in saltaway.push(url):
        print(archive_url)
