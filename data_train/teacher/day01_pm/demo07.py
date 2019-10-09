import numpy as np
import pandas as pd
# pd.read_excel
# pd.read_sql()
# pd.read_html()
# pd.read_json()
df = pd.read_csv("../data/groupby.csv")
print(df,type(df))
ss = df[['Name','Brand']]
print(ss,type(ss))
print('-'*100)
df = pd.read_csv("../data/groupby.csv")
# 查看数据结构
df.info()
# 查询前3条记录默认是5条
print(df.head(n=3))
print('对样本进行分组和聚合操作............')
# 计算每种品牌有多少件衣服
data_group = df.groupby(by="Brand")
# 先分组在调用聚合函数
for index,row in data_group:
    print(index)
    print(row)
# 聚合函数会对每一列进行统计
print(data_group.count())
# sum 只能对符合条件的数据类型(int float)进行操作
print(data_group.sum())
print('基于Series分组和聚合使用')
data_group = df['Count'].groupby(by=df["Brand"])
for index,row in data_group:
    print(index)
    print(row)
print(data_group.sum())




