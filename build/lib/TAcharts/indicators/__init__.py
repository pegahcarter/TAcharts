#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os


directory = 'test string'
str_pt1 = f'from .'
str_pt2 = f' import *'

if directory is None:
    directory = os.getcwd()


# Does directory exist
def is_directory(path):
    if os.path.isdir(path):
        return True
    else:
        return False

# Does file exist
def is_file(path):
    if os.path.isfile(path):
        return True
    else:
        return False


for pyfile in os.listdir(directory):
    # only look at python files that are not __init__ files
    if 'py' in pyfile and '__init__' not in pyfile:


# def create_init(directory=None):






    try:
        pass

    except FileNotFoundError as file_not_found:
        return f''




def loop_through_directory(directory, fn):


    for pyfile in os.listdir(directory)



            package = pyfile[:pyfile.find('.')]
            pyfile_list.append()

            print(''.join([str_pt1, package, str_pt2]))


def relative_import_str(*args):
    return ''.join(arg for arg in args)
