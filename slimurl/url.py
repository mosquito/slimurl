# encoding: utf-8
import re
import sys
from functools import wraps
from .protocols import DEFAULT_PORTS

if sys.version_info < (3,):
    from urllib import quote, unquote
else:
    from functools import reduce
    from urllib.parse import quote, unquote


def _convert_compare(func):
    @wraps(func)
    def wrap(self, other):
        return func(self, URL(other))
    return wrap


class URL(str):
    _fields = frozenset({'scheme', 'user', 'password', 'host', 'path', 'port', 'query', 'fragment'})

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

        def check(part):
            t = part.split("=", 1)
            len(t) < 2 and t.append(None)
            return tuple(t)

        if not query:
            return set([])
        if "&" in query:
            return {check(i) for i in query.split("&")}

        return {check(query)}

    def _parse_port(self, parts):
        port = parts['port'] or DEFAULT_PORTS.get(parts['scheme'])
        return int(port) if port else port

    _POST_PARSERS = {
        'port': _parse_port,
        'query': _split_query,
    }

    def __format_scheme(self, scheme):
        return "{0}://".format(self.__to_string(scheme)) if scheme else ''

    def __format_credentials(cls, username=None, password=None):
        credentials = ":".join((cls.__to_string(username), cls.__to_string(password))).rstrip(':')
        return "{0}@".format(credentials) if credentials else ''

    @staticmethod
    def __format_port(port, scheme):
        return '' if not port or port is DEFAULT_PORTS.get(scheme) else ":{}".format(port)

    def __format_path(self, path):
        if not path:
            return '/'

        return self.__to_string(('{0}' if path.startswith("/") else '/{0}').format(path))

    @staticmethod
    def __format_host(host):
        return str(host) if host else ''

    @staticmethod
    def __format_fragment(fragment):
        return "#%s" % fragment if fragment else ''

    def __to_string(self, item):
        if not item:
            return ''

        if isinstance(item, bytes):
            item = item.decode('utf-8')

        return quote(str(item), safe=self.__safe_symbols)

    @staticmethod
    def __from_string(item):
        if not item:
            return item

        return unquote(item)

    def __format_query(self, query):
        if not query:
            return ''

        params = ("=".join((self.__to_string(key), self.__to_string(value))) for key, value in query)
        return "?{0}".format("&".join(params))

    def __init__(self, url=None, safe_symbols="/\\:", **defaults):
        super(URL, self).__init__()
        self.scheme = None
        self.user = None
        self.password = None
        self.host = None
        self.path = None
        self.port = None
        self.query = set([])
        self.fragment = None
        self.__safe_symbols = safe_symbols

        if not url:
            return

        m = self.EXP.match(str(url))
        if m is None:
            raise ValueError('URL "%r" is not valid' % url)

        url_parts = {key: self.__from_string(value) for key, value in m.groupdict().items()}

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

    def __str__(self):
        url = "".join((
                self.__format_scheme(self.scheme),
                self.__format_credentials(self.user, self.password),
                self.__format_host(self.host),
                self.__format_port(self.port, self.scheme),
                self.__format_path(self.path),
                self.__format_query(self.query),
                self.__format_fragment(self.fragment)
        ))

        return '' if url == '/' else url

    def __call__(self, **kwargs):
        for key, value in ((k, v) for k, v in kwargs.items() if k in self._fields):
            setattr(self, key, value)

        return self

    def __copy__(self):
        return URL(str(self))

    def __repr__(self):
        return '<URL: "%s">' % self

    def __setattr__(self, key, value):
        if key not in self._fields and not key.startswith('_'):
            raise AttributeError('"{}" is not allowed'.format(key))

        return super(URL, self).__setattr__(key, value)

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self):
        yield self.scheme
        yield self.user
        yield self.password
        yield self.host
        yield self.port
        yield "/%s" % self.path.lstrip("/") if self.path else '/'
        yield tuple(sorted((str(k), str(v) if v is not None else '') for k, v in self.query))
        yield self.fragment

    def __contains__(self, item):
        for k, _ in self.query:
            if k == item:
                return True

    def __len__(self):
        return len(str(self))

    @_convert_compare
    def __eq__(self, other):
        return tuple(self) == tuple(other)

    @_convert_compare
    def __lt__(self, other):
        return tuple(self) < tuple(other)

    @_convert_compare
    def __gt__(self, other):
        return tuple(self) > tuple(other)

    @_convert_compare
    def __ge__(self, other):
        return tuple(self) >= tuple(other)

    @_convert_compare
    def __le__(self, other):
        return tuple(self) <= tuple(other)

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

    @property
    def win_path(self):
        return self.path.lstrip("/").replace("/", "\\").replace("|", ":")
