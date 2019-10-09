# -*- coding: utf-8 -*-
# File  : data_pd.py
# Author: water
# Date  : 2019/7/31

import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
#指定默认字体
mpl.rcParams['font.sans-serif'] = 'SimHei'
mpl.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

# data = pd.read_csv("./groupby.csv",)
# print(data)
# data.info()
# print(data.head(n=4))
#
# data_brand_group = data.groupby(by="Brand")
# print(data_brand_group)
# #count聚合函数只对记录进行计数
# print(data_brand_group.count())
# #sum只对符合条件的列进行求和（数值型列）
# print(data_brand_group.sum())
#
# #转换成series来分组
# print(data['Count'].groupby(by=data['Brand']).sum())

##从seaborn默认网上下载数据
# data = sns.load_dataset('tips')
# data.info()
# print(data.head())

# #比较小费与消费金额是否相关
data = pd.read_csv("./tips.csv",)
# plt.scatter(x=data['total_bill'],y=data['tip'])
# plt.xlabel("total_bill")
# plt.ylabel("小费")
# plt.show()

#比较男性、女性小费是否有差别

male_tips_mean = data[data['sex']=='Male']['tip'].mean()
print("male_tips_mean:",male_tips_mean)
female_tips_mean = data[data['sex']=='Female']['tip'].mean()
print("female_tips_mean:",female_tips_mean)
