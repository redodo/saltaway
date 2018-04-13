# -*- coding: utf-8 -*-
import click
import saltaway


@click.command()
@click.argument('url')
@click.option('-q', is_flag=True, default=False,
              help="Find the most recently archived version of the URL")
@click.option('-I', is_flag=True, default=False, help="Use archive.is")
@click.option('-A', is_flag=True, default=False, help="Use web.archive.org")
def cli(url, q, i, a):
    """Archive web pages at various archives."""

    repos = []
    if a:
        repos.append(saltaway.InternetArchive)
    if i:
        repos.append(saltaway.ArchiveIs)

    if len(repos) == 0:
        repos = saltaway.REPOSITORIES

    if q:
        for repo, datetime, archive_url in saltaway.pull(url, repos=repos):
            click.echo("{} {}".format(datetime.isoformat(), archive_url))

    else:
        for repo, archive_url in saltaway.push(url, repos=repos):
            click.echo(archive_url)
