#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages
import slimurl as module

setup(
    name='slimurl',
    version=module.__version__,
    author=module.__author__,
    author_email=module.author_email,
    license="MIT",
    description="SlimURL - Fast library for parsing and building URL addresses",
    platforms="all",
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
)
