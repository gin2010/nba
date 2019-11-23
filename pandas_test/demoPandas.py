# -*- coding: utf-8 -*-
# File  : demoPandas.py
# Author: water
# Date  : 2019/11/19


import pandas as pd
import numpy as np


# 新建时间顺序的索引
dates = pd.date_range("2019-11-1",periods=6)
# 生成6行4列数据，列名为ABCD、索引为dates
datas = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list("ABCD"))
# 重新定义索引为前四个列，并增加EF列
data1 = datas.reindex(index=dates[0:4],columns=list("ABCDEF"))
# 这样重置会出问题，暂未分析出是什么原因导致的
datas.reindex(index=['2019-11-01'],columns=list(datas.columns))
# 查询2019-11-02到2019-11-03的数据
data1["2019-11-02":"2019-11-03"]
