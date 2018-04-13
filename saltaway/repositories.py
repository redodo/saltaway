# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import lxml.html
import requests
import pendulum

from .exceptions import RepositoryFailure, ArchivalFailure
from .utils import parse_duration


_NONE_DURATION = pendulum.Interval()


class Repository:

    #: The name of the repository
    name = None

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64)'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': self.user_agent,
        }

    def push(self, url, max_age=0):
        max_age = parse_duration(max_age)
        if max_age > _NONE_DURATION:
            datetime, location = self.pull(url)
            if datetime > pendulum.now() - max_age:
                return location

        return self._push(url)

    def _push(self, url):
        """Archives the resource in this repository.

        :param url: the URL of the resource that should be archived
        :return: the link to the archived resource
        """
        raise NotImplementedError(
            "'push' method not implemented by repository '%s'"
            % self.__class__.__name__
        )

    def pull(self, url):
        return self._pull(url)

    def _pull(self, url):
        """Returns the latest archived version of a resource.

        :param url: the URL of the resource
        :return: a tuple containing the date and URL of the latest
            archived version of the resource
        """
        raise NotImplementedError(
            "'latest' method not implemented by repository '%s'"
            % self.__class__.__name__
        )


class ArchiveIs(Repository):

    name = 'archive.is'

    def _push(self, url):
        submit_id = self._get_submit_id()
        r = self.session.post('http://archive.is/submit/', data={
            'url': url,
            'anyway': '1',
            'submitid': submit_id,
        })

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            raise ArchivalFailure(e)

        if 'Refresh' in r.headers:
            try:
                return r.headers['Refresh'].split(';url=')[1]
            except IndexError:
                raise ArchivalFailure(
                    "could not find archive URL in Refresh header: '%s'"
                    % r.headers['Refresh']
                )
        elif 'Location' in r.headers:
            return r.headers['Location']
        else:
            for redirect in r.history:
                if 'Location' in redirect.headers:
                    return redirect.headers['Location']

    def _get_submit_id(self):
        r = self.session.get('http://archive.is/')

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            raise ArchivalFailure(e)

        html = lxml.html.fromstring(r.text)
        for form in html.forms:
            if '/submit' in form.action:
                form_data = dict(form.form_values())
                try:
                    return form_data['submitid']
                except KeyError:
                    raise RepositoryFailure(
                        self,
                        "could not find a 'submit_id' in the request form",
                    )

    def _pull(self, url):
        """Pulls the latest archived version of a URL from archive.is.

        The datetime returned from this function is not entirely exact,
        because it misses the seconds. An extra HEAD request to the
        archive URL would be needed to get an exact datetime.

        :param url: the URL of the resource to find
        :return: tuple with a Pendulum datetime, and an archive URL
        """
        r = self.session.get('http://archive.is/' + url)
        html = lxml.html.fromstring(r.text)

        try:
            link = html.xpath('(//*[@id="row0"]/*[@class="THUMBS-BLOCK"]/*/a)[last()]')[0]
            location = link.get('href')
            formatted_datetime = link.xpath('div')[0].text_content()

            datetime = pendulum.from_format(
                formatted_datetime,
                '%d %b %Y %H:%M',
                formatter='classic',
            )

            return datetime, location
        except IndexError:
            return None, None


class InternetArchive(Repository):

    name = 'web.archive.org'

    def _push(self, url):
        r = self.session.get('https://web.archive.org/save/' + url)
        r.raise_for_status()

        if 'Location' in r.headers:
            return r.headers['Location']
        elif 'Content-Location' in r.headers:
            return 'https://web.archive.org' + r.headers['Content-Location']
        else:
            for redirect in r.history:
                if 'Location' in redirect.headers:
                    return redirect.headers['Location']
                elif 'Content-Location' in redirect.headers:
                    return redirect.headers['Content-Location']

    def _pull(self, url):
        r = self.session.head(
            'https://web.archive.org/web/' + url,
            allow_redirects=False,
        )
        location = r.headers['Location']

        formatted_datetime = urlparse(location).path.split('/').pop(2)
        datetime = pendulum.from_format(
            formatted_datetime,
            'YYYYMMDDHHmmss',
            formatter='alternative',
        )
        return datetime, location
