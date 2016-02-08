# encoding: utf-8
from .url import URL

__all__ = ['URL']

aurhor_info = ("Dmitry Orlov", "me@mosquito.su")
version_info = (0, 6, 2)

__version__ = ".".join(map(str, version_info))
__author__ = "{0} <{1}>".format(*aurhor_info)
