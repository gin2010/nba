# -*- coding: utf-8 -*-
# File  : data_pd03.py
# Author: water
# Date  : 2019/8/1
import pandas as pd
import numpy as np
import random
from sklearn.metrics import mean_squared_error

data = pd.read_excel('./user.xls')
data.info()
print(data.head())

print(data.shape)



