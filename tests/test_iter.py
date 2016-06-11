#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_iter(url, result):
    for item1, item2 in zip(url, result):
        assert item1 == item2, "%r != %r" % (item1, item2)


def test_iter():
    cases = [
        [
            "http://user:password@example.net:90/test?foo=bar#spam",
            (
                'http',
                'user',
                'password',
                'example.net',
                90,
                '/test',
                (('foo', 'bar'),),
                'spam'
            )
        ],
    ]

    for url, result in cases:
        yield check_iter, URL(url), result
