# -*- coding: utf-8 -*-
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
    parts = [(float(e[:-1]), e[-1]) for e in value.split()]

    duration_input = {}
    for length, char in parts:
        try:
            denomination = _TIME_DENOMINATIONS[char]
            duration_input[denomination] = length
        except KeyError:
            raise ValueError("unknown time denomination '%s'" % char)

    return pendulum.Interval(**duration_input)


def parse_duration(value):
    if isinstance(value, int):
        return pendulum.interval(seconds=value)
    if isinstance(value, (timedelta, pendulum.Interval,)):
        return pendulum.interval.instance(value)
    if isinstance(value, str):
        return duration_from_string(value)
