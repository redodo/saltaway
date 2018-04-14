# -*- coding: utf-8 -*-
from datetime import timedelta

import pytest
from pendulum import Interval

from saltaway.utils import duration_from_string, parse_duration


def test_duration_from_string():
    assert Interval(seconds=1) == duration_from_string('1s')
    assert Interval(minutes=1) == duration_from_string('1m')
    assert Interval(hours=1) == duration_from_string('1h')
    assert Interval(days=1) == duration_from_string('1d')
    assert Interval(weeks=1) == duration_from_string('1w')

    assert Interval(seconds=14) == duration_from_string('14s')
    assert Interval(weeks=1, days=4) == duration_from_string('1w 4d')
    assert Interval(hours=1, minutes=45) == duration_from_string('1h 45m')

    assert Interval(days=3, hours=16) == duration_from_string('3d16h')

    with pytest.raises(ValueError):
        duration_from_string('1y')
    with pytest.raises(ValueError):
        duration_from_string('40K')
    with pytest.raises(ValueError):
        duration_from_string('one week')


def test_parse_duration():
    assert Interval(minutes=1) == parse_duration(60)
    assert Interval(seconds=40) == parse_duration(40)
    assert Interval(seconds=12.5) == parse_duration(12.5)

    assert Interval(seconds=60) == parse_duration(Interval(seconds=60))
    assert Interval(days=1) == parse_duration(timedelta(days=1))

    assert Interval(minutes=30) == parse_duration('30m')

    with pytest.raises(ValueError):
        parse_duration('three quarters 4 minutes')
    with pytest.raises(ValueError):
        parse_duration({'duration': 40})
