#!/usr/bin/env python
# encoding: utf-8
from collections import namedtuple

from slimurl import URL

TestURL = namedtuple(
    "TestURL",
    ('scheme', 'user', 'password', 'host', 'path', 'port', 'query', 'fragment')
)

EXAMPLES = {
    (
        'http://example.net',
        TestURL(
            scheme='http', host='example.net', port=80, path=None, query=tuple(),
            user=None, password=None, fragment=None
        )
    ),
    (
        'http://example.net/',
        TestURL(
            scheme='http', host='example.net', port=80, path='/', query=tuple(),
            user=None, password=None, fragment=None
        )
    ),
    (
        'http://example.net/foo_path',
        TestURL(scheme='http', host='example.net', port=80, path='/foo_path', query=tuple(),
                user=None, password=None, fragment=None)
    ),
    (
        'http://example.net/foo_path/',
        TestURL(scheme='http', host='example.net', port=80, path='/foo_path/', query=tuple(),
                user=None, password=None, fragment=None)
    ),
    (
        'http://example.net/?foo=bar',
        TestURL(scheme='http', host='example.net', port=80, path='/', query=tuple([('foo', 'bar'),]),
                user=None, password=None, fragment=None)
    ),
    (
        'http://example.net/?foo=bar&foo=baz',
        TestURL(
            scheme='http', host='example.net', port=80, path='/',
            user=None, password=None,
            query=tuple([('foo', 'bar'), ('foo', 'baz')]),
            fragment=None
        )
    ),
    (
        'http://example.net/?foo=bar&foo=baz&foo=foo&bar=1',
        TestURL(
            scheme='http', host='example.net', port=80, path='/',
            user=None, password=None, fragment=None,
            query=tuple([
                ('foo', 'bar'),
                ('foo', 'baz'),
                ('foo', 'foo'),
                ('bar', '1'),
            ])
        )
    ),
    (
        'http://example.net/?foo=bar&foo=baz&foo&bar',
        TestURL(
            scheme='http', host='example.net', port=80, path='/',
            user=None, password=None, fragment=None,
            query=tuple([
                ('foo', 'bar'),
                ('foo', 'baz'),
                ('foo', None),
                ('bar', None),
            ])
        )
    ),
    (
        'mysql://example.net/testdb/',
        TestURL(
            scheme='mysql', host='example.net', port=3306, path='/testdb/',
            user=None, password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'http://test@example.net',
        TestURL(
            scheme='http', host='example.net', port=80, path=None,
            user='test', password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'http://test:secret@example.net',
        TestURL(
            scheme='http', host='example.net', port=80, path=None,
            user='test', password='secret', fragment=None,
            query=tuple()
        )
    ),
    (
        'http://test:secret@example.net:8080',
        TestURL(
            scheme='http', host='example.net', port=8080, path=None,
            user='test', password='secret', fragment=None,
            query=tuple()
        )
    ),
    (
        'unix:///',
        TestURL(
            scheme='unix', host=None, port=None, path='/',
            user=None, password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'unix://',
        TestURL(
            scheme='unix', host=None, port=None, path=None,
            user=None, password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'unix:///var/run/program.sock',
        TestURL(
            scheme='unix', host=None, port=None, path='/var/run/program.sock',
            user=None, password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'unix:///var/run/program.sock?foo=bar',
        TestURL(
            scheme='unix', host=None, port=None, path='/var/run/program.sock',
            user=None, password=None, fragment=None,
            query=tuple(
                [('foo', 'bar')]
            )
        )
    ),
    (
        'http://[::]:80/',
        TestURL(
            scheme='http', host='[::]', port=80, path='/',
            user=None, password=None, fragment=None,
            query=tuple()
        )
    ),
    (
        'http://user:pass@[::]:80/path/?url#sdfs',
        TestURL(
            scheme='http', host='[::]', port=80, path='/path/',
            user='user', password='pass', fragment='sdfs',
            query=tuple([('url', None)])
        )
    ),
}

NORM_MAP = {
    tuple: set
}


def normalize(value):
    return NORM_MAP.get(type(value), lambda x: x)(value)


def check_url(url_string, url_test):
    url = URL(url_string)
    for attr in url_test._fields:
        url_attr = getattr(url, attr)
        test_value = normalize(getattr(url_test, attr))
        assert url_attr == test_value, "({} != {})[{}] {} != {}".format(url, url_string, attr, url_attr, test_value)


def test_url():
    for url_string, url_test in EXAMPLES:
        yield check_url, url_string, url_test
