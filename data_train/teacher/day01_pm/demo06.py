import numpy as np
import pandas as pd

# Series 是表的列(特征)
ss = pd.Series(data=np.arange(4,8),index=list('abcd'),name='title')
print(ss,type(ss))
print(ss.index,ss.values,type(ss.values))
# 创建一个DataFrame
df = pd.DataFrame(data=np.arange(12).reshape(3,4),index=list('abc'),columns=list('xyzw'))
print(df,type(df))
print(df.index,df.values,type(df.values))
