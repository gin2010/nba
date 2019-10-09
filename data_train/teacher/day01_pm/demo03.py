import numpy as np
# 矩阵元素的获取，和四则运算操作
t1 = np.arange(12).reshape(3,4)
print(t1,t1.shape)
# 默认下标获取行
print(t1[0])
# [行:,列:]  : 连续的行与列
print(t1[0:2,1:])
# 获取连续的行和不连续的列
print(t1[:,(1,3)])
# 获取多个矩阵的数据
# (0,1)  (2,3)
print(t1[(0,2),(1,3)])
# 获取不连续的行与列
t2 = t1[:,(1,3)]
print(t2[(0,2),:])

