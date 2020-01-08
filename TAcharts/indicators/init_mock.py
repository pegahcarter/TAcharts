#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os

if directory is None:
    directory = os.getcwd()


# For testing
directory = '/home/carter/Documents/TAcharts/TAcharts'

myfiles = os.listdir(directory)
myfile = myfiles[0]

pyfile = os.getcwd() + '/' + myfile

foo(pyfile)



os.getcwd()


list(filter(foo, myfiles))

os.path.isfile(pyfile)



def foo(pyfile):

    if '__init__' not in pyfile and 'py' in pyfile:
        if os.path.isdir(pyfile):
            return f'from . import {pyfile} as {pyfile}'
        elif os.path.isfile(pyfile):
            return f'from .{pyfile[:pyfile.find(".")]} import *'
        else:
            return f'This file is not recognized as a file or directory:  {pyfile}'
            # Timestamp of Easter Egg: 2019.01.08 1:54am
            raise AssertionError(f'Error: Call Carter at (916) 477-5363 for further instruction')




def loop_through_directory(directory):

    statements = [f'from .{filename[:filename.find(".")]} import *' \
                for filename in sorted(os.listdir(directory)) \
                # only look at python files that are not __init__ files
                if 'py' in filename \
                and '__init__' not in filename \
                and os.path.isfile(directory + '/' + filename)]

    return statements


# Code to auto-generate import files
myList = loop_through_directory(os.getcwd())

with open(os.getcwd() + '/' + '__init__.py', 'w') as pyfile:
    pyfile.write('\n'.join(myList))
