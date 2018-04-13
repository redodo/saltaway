# -*- coding: utf-8 -*-
import click
import saltaway


@click.command()
@click.argument('url')
@click.option('--find', '-f', is_flag=True, default=False,
              help="Find the most recently archived version of the URL")
def cli(url, find):

    if find:
        for repo, datetime, archive_url in saltaway.pull(url):
            click.echo("{} | {}".format(datetime.isoformat(), archive_url))

    else:
        for repo, archive_url in saltaway.push(url):
            click.echo(archive_url)
