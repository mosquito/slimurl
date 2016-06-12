#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL
from tests.test_url import EXAMPLES


def check_str(url):
    assert str(url) == url, "%s != %s" % (url, url)


def test_str():
    for url_string, _ in EXAMPLES:
        yield check_str, URL(url_string)
