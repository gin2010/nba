# -*- coding: utf-8 -*-
# File  : demoPandas.py
# Author: water
# Date  : 2019/11/19


import pandas as pd
import numpy as np

# 创建数组方式
data = np.arange(1,5).reshape(2,2)
data = np.array(data,dtype=float) # 转换数据类型为float
data = np.array([[1,3,5,7],
                 [2,4,6,8],
                 [3,6,9,12],
                 [4,8,16,32]])
# 数组的形状
data.shape
# 数组里元素的类型
data.dtype
# 数组第二行
data[1]
# 数组第二列
data[:,1]
# 数组(2,2)元素的值
data[1,1]
# 筛选>=8元素组成的一维数组
data[data>=8]
# 矩阵的转置
x=np.arange(1,5).reshape(2,2)
x.T
# 返回固定间隔的数据
np.linspace(0,100,20)
np.linspace(0,100,3)  # ==>返回 [0,50,100]

##pandas



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
# 查询2019-11-02到2019-11-03的E列数据
datas.loc[date[1:3],'E']
# 2019-11-02到2019-11-03的E列的值设为10
datas.loc[date[1:3],'E']=10
# np.nan值的处理--删除有na值的数据所在的行
datas.dropna()
# np.nan值的处理--填充为11
datas.fillna(value =11)
# 判断每个数据是不是na，返回T/F
pd.isnull(datas)
# 判断每列里有没有na值，如果有的话就返回T
pd.isnull(datas).any()
# 判断datas里有没有na值，如果有的话就返回T
pd.isnull(datas).any().any()
# 对数据每列求平均值
datas.mean()
# 对数据每行求平均值
datas.mean(axis=1)
# 对数据每列从第一个元素开始往下累加
datas.cumsum()
datas.apply(np.cumsum)

# 创建一个series
data1 = pd.Series([1,3,5,np.nan,9,11],index=date)
# shift是上下移到，如果是正数则表示下移两位，前两位默认用na来填充
data1 = pd.Series([1,3,5,np.nan,9,11],index=date).shift(2)
# datas减data1，索引为datas的index,得到与datas一样的数据结构，na值的结果仍为na
datas.sub(data1,axis="index")
# 对datas的每列求出最大值与最小值的差
datas.apply(lambda x:x.max()-x.min())
# 生成随机10--20的series，大小为20
s1 = pd.Series(np.random.randint(10,20,size=20))
# 统计s1中每个值出现的次数
s1.value_counts()
# 统计s1中哪个数出现的次数最多
s1.mode()

# 数据透视表values代表值、index代表索引、columns代表列名（按列里面值进行分类）
datas.pivot(values=['C'],index=['A','B'],columns=['D'])

# 时间序列--按秒生成时间序列
date = pd.date_range("2019-11-01",periods=600,freq="s")
s1 = pd.Series(np.random.randint(len(date)),index=date)
# 时间序列--对上面按秒生成的时间序列进行按2分钟为单位进行合并数据（重采样），方法可以为sum/mean
s1.resample("2Min",how="mean")
# 时间序列--生成季度日期
quar = pd.period_range("2000Q1", "2019Q1", freq="Q")
# 季度格式转换为正常日期格式（每个季度第一天所在的日期）
quar.to_timestamp()
# 时间序列--日期的计算，往后180天所在的日期
pd.Timestamp("20190101")+pd.Timedelta(days=180)

# 多重索引
mindex = list(zip(*[['bar','bar','baz','baz','foo','foo','qux','qux'],
                    ['one','two','one','two','one','two','one','two']]))
index = pd.MultiIndex.from_tuples(mindex,names=['first','second'])
datas = pd.DataFrame(np.random.randn(8,2),index=index,columns=['A','B'])
# 行列索引转换
# 列索引转为行索引
data_stack = datas.stack()
# 行索引转为列索引（每次从最末级索引开始转换）
data_unstack = data_stack.unstack()

