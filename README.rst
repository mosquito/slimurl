Slim URL
========

.. image:: https://travis-ci.org/mosquito/slimurl.svg
    :target: https://travis-ci.org/mosquito/slimurl

.. image:: https://img.shields.io/pypi/v/slimurl.svg
    :target: https://pypi.python.org/pypi/slimurl/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/slimurl.svg
    :target: https://pypi.python.org/pypi/slimurl/

.. image:: https://img.shields.io/pypi/pyversions/slimurl.svg
    :target: https://pypi.python.org/pypi/slimurl/

.. image:: https://img.shields.io/pypi/l/slimurl.svg
    :target: https://pypi.python.org/pypi/slimurl/


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

