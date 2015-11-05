#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_pop(url, result, args, kwargs):
    res = url.pop(*args, **kwargs)

    res = tuple(sorted(res)) if isinstance(res, (list, tuple)) else res
    result = tuple(sorted(result)) if isinstance(result, (list, tuple)) else result

    assert res == result, "%r is not %r" % (res, result)


def test_pop():
    cases = [
        ["http://example.net/?foo=bar", 'bar', ['foo'], {}],
        ["http://example.net/?foo=", '', ['foo'], {'default': None}],
        ["http://example.net/?foo", None, ['foo'], {}],
        ["http://example.net/?bar=foo", 'bar', ['foo'], {'default': 'bar'}],
    ]

    for url, result, args, kwargs in cases:
        yield check_pop, URL(url), result, args, kwargs
