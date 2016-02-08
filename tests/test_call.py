#!/usr/bin/env python
# encoding: utf-8
from copy import copy
from slimurl import URL
from tests.test_url import EXAMPLES


def check_call(url):
    clone = copy(url)
    url(path='test')
    clone.path = 'test'

    assert clone == url


def test_call():
    for url_string, _ in EXAMPLES:
        yield check_call, URL(url_string)


def test_init():
    yield lambda: URL("http://localhost/") != URL(None)
    yield lambda: URL("http://localhost/") != URL('')
    yield lambda: URL("http://localhost/") != URL()
    yield lambda: URL("http://localhost/") is not None
    yield lambda: URL("http://localhost/") != ''
