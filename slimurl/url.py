# encoding: utf-8
import re
import sys
from copy import copy
from functools import total_ordering
from .protocols import DEFAULT_PORTS

if sys.version_info < (3,):
    from urllib import quote, unquote
else:
    from functools import reduce
    from urllib.parse import quote, unquote


@total_ordering
class URL(object):

    __slots__ = {'scheme', 'user', 'password', 'host', 'path', 'port', 'query', 'fragment'}

    EXP = re.compile(
        '^(?P<scheme>[^\:]+):\/\/'
        '((((?P<user>[^:^@]+))?'
        '((\:(?P<password>[^@]+)?))?\@)?'
        '(?P<host>([^\/^:]+|\[([^\/]+)\]))'
        '(\:(?P<port>\d+))?)?'
        '(((?P<path>\/[^\?]*)'
        '(\?(?P<query>[^\#]+)?)?'
        '(\#(?P<fragment>.*))?)?)?$'
    )

    def _split_query(self, parts):
        query = parts['query']

        def chk(prt):
            t = prt.split("=", 1)
            len(t) < 2 and t.append(None)
            return tuple(t)

        if not query:
            return set([])
        if "&" in query:
            return {chk(i) for i in query.split("&")}

        return {chk(query)}

    def _parse_port(self, parts):
        port = parts['port'] or DEFAULT_PORTS.get(parts['scheme'])
        return int(port) if port else port

    _POST_PARSERS = {
        'port': _parse_port,
        'query': _split_query,
    }

    def __init__(self, url=None, **defaults):
        self.scheme = None
        self.user = None
        self.password = None
        self.host = None
        self.path = None
        self.port = None
        self.query = set([])
        self.fragment = None

        if not url:
            return

        m = self.EXP.match(str(url))
        if m is None:
            raise ValueError('URL "%r" is not valid' % url)

        url_parts = {key: self._from_string(value) for key, value in m.groupdict().items()}

        for key, value in url_parts.items():
            post_parser = self._POST_PARSERS.get(key)

            setattr(self, key, post_parser(self, url_parts) if post_parser else value)

        for key, value in defaults.items():
            if not getattr(self, key, None):
                setattr(self, key, value)

    def __setitem__(self, key, value):
        if isinstance(value, (tuple, list)):
            for item in value:
                self.query.add((key, str(item)))
        else:
            self.query.add((key, str(value)))

    def __getitem__(self, item):
        return list(map(lambda x: x[1], filter(lambda x: x[0] == item, self.query)))

    def path_append(self, *args, **kwargs):
        path = ''
        escape = kwargs.get('escape', False)

        def arg_filter(result, item):
            if item == '..' and not escape:
                result[0] -= 1
                return result

            if item in ('', '/'):
                result[1].append(None)

            result[1].append(item)
            return result

        parts = (self.path or '/').split("/")[1:]
        shift, args = reduce(arg_filter, args, [len(parts), []])
        parts = parts[:shift] if parts[-1] else parts[:shift - 1] + ['']

        for subset in parts, args:
            for part in subset:
                if not path.endswith("/"):
                    path += "/"

                if part is None:
                    continue

                path += str(part)

        self.path = path

    @staticmethod
    def _to_string(item):
        if not item:
            return ''

        if isinstance(item, bytes):
            item = item.decode('utf-8')

        return quote(str(item))

    @staticmethod
    def _from_string(item):
        if not item:
            return item

        return unquote(item)

    @classmethod
    def _format_query(cls, query):
        if not query:
            return ''

        params = ("=".join((cls._to_string(key), cls._to_string(value))) for key, value in query)
        return "?{0}".format("&".join(params))

    @classmethod
    def _format_scheme(cls, scheme):
        return "{0}://".format(cls._to_string(scheme)) if scheme else ''

    @classmethod
    def _format_credentials(cls, username=None, password=None):
        credentials = ":".join((cls._to_string(username), cls._to_string(password))).rstrip(':')
        return "{0}@".format(credentials) if credentials else ''

    @classmethod
    def _format_port(cls, port, scheme):
        return '' if not port or port is DEFAULT_PORTS.get(scheme) else ":{}".format(port)

    @classmethod
    def _format_path(cls, path):
        if not path:
            return '/'

        return cls._to_string(('{0}' if path.startswith("/") else '/{0}').format(path))

    @staticmethod
    def _format_host(host):
        return str(host) if host else ''

    def __str__(self):
        url = "".join((
                self._format_scheme(self.scheme),
                self._format_credentials(self.user, self.password),
                self._format_host(self.host),
                self._format_port(self.port, self.scheme),
                self._format_path(self.path),
                self._format_query(self.query)
        ))

        return '' if url == '/' else url

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def __copy__(self):
        url = URL()

        for key in self.__slots__:
            setattr(url, key, copy(getattr(self, key)))

        return url

    def __repr__(self):
        return '<URL: "%s">' % self

    def __setattr__(self, key, value):
        if key not in self.__slots__:
            raise AttributeError('"{}" is not allowed'.format(key))

        return super(URL, self).__setattr__(key, value)

    def __hash__(self):
        fields = (
            self.scheme, self.user, self.password, self.host, self.port, self.path if self.path else '/',
            tuple(sorted((str(k), str(v)) for k, v in self.query)), self.fragment
        )

        return hash(fields)

    def __iter__(self):
        yield self.scheme
        yield self.user
        yield self.password
        yield self.host
        yield self.port
        yield self.path or '/'
        yield frozenset(self.query)
        yield self.fragment

    def __contains__(self, item):
        for k, _ in self.query:
            if k == item:
                return True

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        if not isinstance(other, URL):
            other = URL(other)

        return hash(self) == hash(other) and tuple(self) == tuple(other)

    def __lt__(self, other):
        if not isinstance(other, URL):
            other = URL(other)

        return len(self) < len(other)

    def __delitem__(self, key):
        for item in list(sorted(self.query)):
            k, v = item
            if k == key:
                self.query.remove(item)

    def get(self, key, default=None, limit=1):
        assert limit is None or limit > 0 or isinstance(limit, int), \
            "limit might be None or positive integer"

        result = list(
            map(
                lambda x: x[1],
                filter(
                    lambda x: x[0] == key,
                    self.query
                )
            )
        )

        result = result if result else None

        if result:
            if limit is None:
                return result
            else:
                return result[:limit] if limit > 1 else result[0]
        else:
            return default

    def pop(self, key, default=None):
        for item in list(sorted(self.query)):
            k, v = item
            if k == key:
                self.query.remove(item)
                return v

        return default

    def remove_all(self, key):
        while key in self:
            del self[key]

    def remove(self, key):
        self.pop(key)
