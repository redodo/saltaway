# -*- coding: utf-8 -*-
import lxml.html
import requests

from .exceptions import RepositoryFailure, ArchivalFailure


class Repository:

    #: The name of the repository
    name = None

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64)'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': self.user_agent,
        }

    def push(self, url):
        """Archives the resource in this repository.

        :param uri: the URL of the resource that should be archived
        :return: the link to the archived resource
        """
        raise NotImplementedError(
            "'_push' method not implemented by repository '%s'"
            % self.__class__.__name__
        )


class ArchiveIs(Repository):

    name = 'archive.is'

    def push(self, url):
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


class WaybackMachine(Repository):

    name = 'web.archive.org'

    def push(self, url):
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
