# -*- coding: utf-8 -*-
import click
import saltaway

from .utils import parse_duration


class DurationType(click.ParamType):
    name = 'duration'

    def convert(self, value, param, ctx):
        try:
            return parse_duration(value)
        except ValueError as e:
            self.fail(e, param, ctx)


DURATION = DurationType()


@click.command()
@click.argument('url')
@click.option('-q', 'query', is_flag=True, default=False,
              help="Find the most recently archived version of the URL")
@click.option('-A', 'internet_archive', is_flag=True, default=False,
              help="Use web.archive.org")
@click.option('-I', 'archive_is', is_flag=True, default=False,
              help="Use archive.is")
@click.option('--max-age', '-m', default=0, type=DURATION, help=(
    "The maximum allowed age of an existing archive. Can be the amount "
    "of seconds or a value like '1h' or '30m'."))
def cli(url, query, internet_archive, archive_is, max_age):
    """Archive web pages at various archives."""
    repos = []
    if internet_archive:
        repos.append(saltaway.InternetArchive)
    if archive_is:
        repos.append(saltaway.ArchiveIs)

    if len(repos) == 0:
        repos = saltaway.api.REPOSITORIES

    if query:
        for repo, datetime, archive_url in saltaway.pull(url, repos=repos):
            click.echo("{} {}".format(datetime.isoformat(), archive_url))

    else:
        for repo, archive_url in saltaway.push(url, repos=repos, max_age=max_age):
            click.echo(archive_url)
