#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from . import indicators as indicators
from . import utils as utils

from .wrappers import *

import numpy as np
import pandas as pd

# Ignore stupid divide by 0 warnings
np.seterr(divide="ignore", invalid="ignore")

import matplotlib.dates as mdates

pd.plotting.register_matplotlib_converters()
