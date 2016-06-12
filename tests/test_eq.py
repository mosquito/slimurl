#!/usr/bin/env python
# encoding: utf-8
from slimurl import URL
from tests.test_url import EXAMPLES


def check_eq(url_a, url_b, expected_result):
    url_a, url_b = URL(url_a), URL(url_b)
    assert (url_a == url_b) == expected_result, \
        "Unexpected result: %r == %r is not %s" % (url_a, url_b, expected_result)


def test_eq():
    cases = {
        ("http://example.net:80", "http://example.net/", True),
        ("http://example.net:80", "http://example.net", True),
        ("http://example.net:8080", "http://example.net", False),
        ("http://example.net/?bar=foo&foo=bar", "http://example.net/?foo=bar&bar=foo", True),
        ("http://example.net/?bar=foo&foo=bar#test", "http://example.net/?foo=bar&bar=foo#test", True),
    }

    for url_a, url_b, expected_result in cases:
        yield check_eq, url_a, url_b, expected_result
        yield check_eq, url_b, url_a, expected_result


def check_eq_examples(url):
    assert url == url, "%s != %s" % (url, url)


def test_eq_examples():
    for url_string, _ in EXAMPLES:
        yield check_eq_examples, URL(url_string)
