#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_path_append(base, predict, args):
    base = URL(base)
    base.path_append(*args)

    assert base == predict, "%r is not %r" % (base, predict)


def test_path_append():
    cases = [
        ["http://example.net", "http://example.net", []],
        ["http://example.net", "http://example.net/", ['']],
        ["http://example.net", "http://example.net/foo", ['foo']],
        ["http://example.net", "http://example.net/foo/", ['foo', '']],
        ["http://example.net", "http://example.net/foo/bar", ['foo', 'bar']],
        ["http://example.net", "http://example.net/foo/bar/", ['foo', 'bar', '']],
        ["http://example.net", "http://example.net/foo/bar/", ['foo', 'bar', '']],
        ["http://example.net/foo", "http://example.net/foo/bar/", ['bar', '']],
        ["http://example.net/foo/", "http://example.net/foo/bar/", ['bar', '']],
        ["http://example.net/foo/", "http://example.net/foo/bar", ['bar']],
        ["http://example.net/foo/", "http://example.net/foo/", ['']],

        ["http://example.net/foo/", "http://example.net/", ['..']],
        ["http://example.net/foo", "http://example.net/", ['..']],
        ["http://example.net/", "http://example.net/", ['..']],
        ["http://example.net/", "http://example.net/", ['..', '..']],
        ["http://example.net/", "http://example.net/", ['..', '..', '..']],
        ["http://example.net/foo/bar/baz/", "http://example.net/", ['..', '..', '..']],
        ["http://example.net/foo/bar/baz", "http://example.net/", ['..', '..', '..']],
        ["http://example.net/foo/bar/baz/", "http://example.net/foo/", ['..', '..']],
        ["http://example.net/foo/bar/baz", "http://example.net/foo", ['..', '..']],

        ["http://example.net/foo/", "http://example.net/foo/", []],
    ]

    for url, predict, args in cases:
        yield check_path_append, URL(url), URL(predict), args
