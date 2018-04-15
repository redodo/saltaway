# -*- coding: utf-8 -*-
import os
import pickle
from hashlib import sha256

import requests
import pendulum


TEST_URL = 'http://example.org'

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
CACHE_DIR = os.path.join(TESTS_DIR, '.cache')

CACHE_DURATION = pendulum.Interval(days=1)


class CachedSession(requests.Session):
    """Caches all responses.

    The only way to check if Saltaway's archival implementation is
    still functional, is to actually trigger the archival of a web
    page. This only has to happen once per test run across different
    Python versions and dependencies.
    """

    def request(self, *args, **kwargs):
        cache_key = sha256(pickle.dumps((args, kwargs))).hexdigest()
        cache_filename = os.path.join(CACHE_DIR, cache_key)

        try:
            # Get the response from cache
            with open(cache_filename, 'rb') as f:
                ts, response = pickle.load(f)
                if ts + CACHE_DURATION < pendulum.now():
                    raise FileNotFoundError()
                else:
                    return response
        except (FileNotFoundError, EOFError, ValueError):
            pass

        # Execute the request and cache it
        response = super().request(*args, **kwargs)
        response.close()
        with open(cache_filename, 'wb') as f:
            pickle.dump((pendulum.now(), response), f)
        return response


# Monkey patch the Session class to the CachedSession
requests.session = requests.Session = CachedSession

os.makedirs(CACHE_DIR, exist_ok=True)
