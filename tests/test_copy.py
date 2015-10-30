#!/usr/bin/env python
# encoding: utf-8
from copy import copy
from slimurl import URL
from tests.test_url import EXAMPLES


def check_copy(original):
    clone = copy(original)
    clone.host = 'example.com'

    assert original.host != clone.host


def test_copy():
    for url_string, _ in EXAMPLES:
        yield check_copy, URL(url_string)