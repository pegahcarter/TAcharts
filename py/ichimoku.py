from TAcharts.py.utils import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import matplotlib.pyplot as plt


class Ichimoku:
    def __init__(self, FILE='data/15min.csv'):
        self.df = pd.read_csv(FILE)


    def build(self):
        pass

    def _apply_renko(self):
        pass


    def plot(self):
        fig, ax = plt.subplots(figsize=(20,20))
