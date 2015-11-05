#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_set(url, args, result):
    key, value = args

    url[key] = value

    assert url == result


def test_set():
    cases = [
        ["http://example.net/", ('foo', 'bar'), "http://example.net/?foo=bar"],
        ["http://example.net/", ('foo', (0, 1)), "http://example.net/?foo=0&foo=1"],
        ["http://example.net/", ('foo', ("0", "1")), "http://example.net/?foo=0&foo=1"],
        ["http://example.net/", ('foo', (0, "1")), "http://example.net/?foo=0&foo=1"],
    ]

    for url, args, result in cases:
        yield check_set, URL(url), args, URL(result)
