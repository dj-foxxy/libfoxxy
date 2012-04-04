#!/usr/bin/env python2
from distutils.core import setup

setup(
    name='libfoxxy',
    version='0.0',
    description="Foxxy's utility library.",

    author='Peter Sutton',
    author_email='petersutton2009@gmail.com',
    url='http://petersutton.me/',

    package_dir={'': 'src'},
    packages=(
        'foxxy',
        'foxxy.threading'
    ),
)

