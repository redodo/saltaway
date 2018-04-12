# -*- coding: utf-8 -*-
import click
import saltaway


@click.command()
@click.argument('url')
def cli(url):
    for repo, archive_url in saltaway.push(url):
        click.echo(archive_url)
