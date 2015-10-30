# encoding: utf-8
import string
from random import choice, randint
from slimurl import URL
from slimurl.url import quote


MIN_LENGTH = 3
MAX_LENGTH = 30


def gen_string(max_len=None, dictionary=None):
    if max_len is None:
        max_len = randint(MIN_LENGTH, MAX_LENGTH)

    if dictionary is None:
        dictionary = list(quote(letter) for letter in string.printable if letter != '/')

    return "".join(choice(dictionary) for _ in range(max_len))


def gen_path(repeats=None):
    if repeats is None:
        repeats = randint(MIN_LENGTH, MAX_LENGTH)

    return "{0}".format("/".join(gen_string()) for _ in range(repeats))


def gen_query(repeats=None):
    if repeats is None:
        repeats = randint(MIN_LENGTH, MAX_LENGTH)

    types = (
        lambda: "{0}=".format(gen_string()),
        lambda: "{0}".format(gen_string()),
        lambda: "{0}={1}".format(gen_string(), gen_string()),
    )

    return "&".join(choice(types)() for _ in range(repeats))


def gen_urls():
    repeats = 20

    for x in range(repeats):
        data = dict(
            scheme=gen_string(randint(2, 10), string.ascii_lowercase),
            user=gen_string(randint(1, MAX_LENGTH)),
            passwd=gen_string(randint(1, MAX_LENGTH)),
            host=gen_string(randint(2, MAX_LENGTH)),
            port=randint(1, MAX_LENGTH),
            path=gen_path(),
            query=gen_query(),
            anchor=gen_string(randint(0, MAX_LENGTH)),
        )

        types = (
            "{scheme}://{user}:{passwd}@{host}:{port}/{path}?{query}#{anchor}",
            "{scheme}://{user}:{passwd}@{host}:{port}/{path}?{query}",
            "{scheme}://{user}:{passwd}@{host}:{port}/{path}?#",
            "{scheme}://{user}:{passwd}@{host}:{port}/?#",
            "{scheme}://{user}:{passwd}@{host}:{port}/?",
            "{scheme}://{user}:{passwd}@{host}:{port}/#",
            "{scheme}://{user}:{passwd}@{host}:{port}/",
            "{scheme}://{user}:{passwd}@{host}:{port}",
            "{scheme}://{user}:{passwd}@{host}/{path}?{query}#{anchor}",
            "{scheme}://{user}:{passwd}@{host}/{path}?{query}",
            "{scheme}://{user}:{passwd}@{host}/{path}?#",
            "{scheme}://{user}:{passwd}@{host}/?#",
            "{scheme}://{user}:{passwd}@{host}/?",
            "{scheme}://{user}:{passwd}@{host}/#",
            "{scheme}://{user}:{passwd}@{host}/",
            "{scheme}://{user}:{passwd}@{host}",
            "{scheme}://{user}@{host}/{path}?{query}#{anchor}",
            "{scheme}://{user}@{host}/{path}?{query}",
            "{scheme}://{user}@{host}/{path}?#",
            "{scheme}://{user}@{host}/?#",
            "{scheme}://{user}@{host}/?",
            "{scheme}://{user}@{host}/#",
            "{scheme}://{user}@{host}/",
            "{scheme}://{user}@{host}",
            "{scheme}://:{passwd}@{host}/{path}?{query}#{anchor}",
            "{scheme}://:{passwd}@{host}/{path}?{query}",
            "{scheme}://:{passwd}@{host}/{path}?#",
            "{scheme}://:{passwd}@{host}/?#",
            "{scheme}://:{passwd}@{host}/?",
            "{scheme}://:{passwd}@{host}/#",
            "{scheme}://:{passwd}@{host}/",
            "{scheme}://:{passwd}@{host}",
            "{scheme}://@{host}/{path}?{query}#{anchor}",
            "{scheme}://@{host}/{path}?{query}",
            "{scheme}://@{host}/{path}?#",
            "{scheme}://@{host}/?#",
            "{scheme}://@{host}/?",
            "{scheme}://@{host}/#",
            "{scheme}://@{host}/",
            "{scheme}://@{host}",
            "{scheme}://{host}/{path}?{query}#{anchor}",
            "{scheme}://{host}/{path}?{query}",
            "{scheme}://{host}/{path}?#",
            "{scheme}://{host}/?#",
            "{scheme}://{host}/?",
            "{scheme}://{host}/#",
            "{scheme}://{host}/",
            "{scheme}://{host}",
            "{scheme}:///{path}?{query}#{anchor}",
            "{scheme}:///{path}?{query}",
            "{scheme}:///{path}?#",
            "{scheme}:///?#",
            "{scheme}:///?",
            "{scheme}:///#",
            "{scheme}:///",
            "{scheme}://",
        )

        for fmt in types:
            yield fmt.format(**data)


def test_url():
    for url in gen_urls():
        yield URL, url

