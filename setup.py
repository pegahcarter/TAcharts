#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import os.path
import codecs
import setuptools

# Get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()


setuptools.setup(
  name = 'TAcharts',
  version = '0.0.16',
  author = 'Carter Carlson',
  author_email = 'carlfarterson@gmail.com',
  license = 'MIT',
  description = 'TA Charting tool',
  keywords=['TA', 'mathematics', 'algorithms'],
  long_description=long_description,
  long_description_content_type='text/markdown',
  url = 'https://github.com/carlfarterson/TAcharts',
  packages=setuptools.find_packages(),
  download_url = 'https://github.com/carlfarterson/TAcharts/archive/v_0.0.1.tar.gz',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers'
  ],
  python_requires='>=3.6'
)
