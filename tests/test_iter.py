#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL


def check_iter(url, result):
    scheme1, user1, password1, host1, port1, path1, query1, fragment1 = url
    scheme2, user2, password2, host2, port2, path2, query2, fragment2 = result
    assert scheme1 == scheme2
    assert user1 == user2
    assert password1 == password2
    assert host1 == host2
    assert port1 == port2
    assert path1 == path2
    assert tuple(sorted(query1)) == tuple(sorted(query2))
    assert fragment1 == fragment2


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
                [('foo', 'bar')],
                'spam'
            )
        ],
    ]

    for url, result in cases:
        yield check_iter, URL(url), result
