#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import os.path
import codecs  # To use a consistent encoding
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# Package name
pname = 'TAcharts'

# Get the version
version = 0.1

# Generate links
gurl = 'https://github.com/carlfarterson/' + pname
download_url = gurl + '/tarball/' + __version__


setuptools.setup(
    name=pname,
    version=version,

    description='TA Charting tool',
    long_description = long_description,


)
