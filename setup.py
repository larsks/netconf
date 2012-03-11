#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = "netconf",
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@seas.harvard.edu',
    version = "1",
    packages = find_packages(),
    scripts = [ 'bin/netconf' ],
)
