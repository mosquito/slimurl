#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_win_path(url, expected_result):
    assert url.win_path == expected_result, "%r != %r" % (url.win_path, expected_result)


def test_win_path():
    cases = {
        ('file://localhost/c|/WINDOWS/clock.avi', "c:\\WINDOWS\\clock.avi"),
        ('file:///c|/WINDOWS/clock.avi', "c:\\WINDOWS\\clock.avi"),
        ('file://localhost/c:/WINDOWS/clock.avi', "c:\\WINDOWS\\clock.avi"),
        ('file:///c:/WINDOWS/clock.avi', "c:\\WINDOWS\\clock.avi"),
    }

    for url, expected_result in cases:
        yield check_win_path, URL(url), expected_result
