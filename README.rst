Slim URL
========

.. image:: https://travis-ci.org/mosquito/slimurl.svg
    :target: https://travis-ci.org/mosquito/slimurl

Slim URL - is fast wrapper for construction or/and parse URL components. Parsing based on regular expressions.

Example::

    from slimurl import URL

    url = URL('http://example.net')
    print("%r" % url)
    # <URL "http://example.net/">

    print((url.host, url.port, url.scheme))
    # ('example.net', 80, 'http')

    URL('http://example.net') == URL('http://example.net/')
    # True

    URL('http://example.net:80') == URL('http://example.net/')
    # True

    URL('http://example.net') == URL('http://example.net/?foo=bar')
    # False

