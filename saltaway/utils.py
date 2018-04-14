# -*- coding: utf-8 -*-
import itertools
from datetime import timedelta

import pendulum


_TIME_DENOMINATIONS = {
    's': 'seconds',
    'm': 'minutes',
    'h': 'hours',
    'd': 'days',
    'w': 'weeks',
}


def duration_from_string(value):
    value = value.replace(' ', '')
    parts = [''.join(e) for _, e in itertools.groupby(value, key=str.isdigit)]

    if len(parts) % 2 != 0:
        raise ValueError("Incorrect duration format")

    # map lengths to denominations
    parts = zip(parts[::2], parts[1::2])

    duration_input = {}
    for length, char in parts:
        try:
            denomination = _TIME_DENOMINATIONS[char]
            duration_input[denomination] = float(length)
        except KeyError:
            raise ValueError("Unknown time denomination '%s'" % char)

    return pendulum.Interval(**duration_input)


def parse_duration(value):
    if isinstance(value, (int, float)):
        return pendulum.interval(seconds=value)
    if isinstance(value, (timedelta, pendulum.Interval)):
        return pendulum.interval.instance(value)
    if isinstance(value, str):
        return duration_from_string(value)
    raise ValueError("Could not parse value '%s' as a duration" % value)
