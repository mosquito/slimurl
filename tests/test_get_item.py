#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_get(url, key, value):
    assert url[key] == value, "%r is not %r" % (url[key], value)


def test_get():
    cases = [
        ["http://example.net/?foo=bar", 'foo', ['bar']],
    ]

    for url, key, value in cases:
        yield check_get, URL(url), key, value
