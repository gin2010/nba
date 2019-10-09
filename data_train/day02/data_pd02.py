# -*- coding: utf-8 -*-
# File  : data_pd02.py
# Author: water
# Date  : 2019/8/1

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
#指定默认字体
mpl.rcParams['font.sans-serif'] = 'SimHei'
mpl.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


data = pd.read_csv("./tips.csv")
print(data.info())
print(data.head())
#
# data_groupby_day = data['total_bill'].groupby(by=data['day']).sum()
# plt.bar(data_groupby_day.index,data_groupby_day.values,color= "#ff0000")
# plt.show()

data_time = data['time'].value_counts()
print(data_time,type(data_time))
plt.pie(data_time.values)
plt.show()