import numpy as np
# 矩阵运算和筛选 (矩阵运算就是矩阵的每个元素单独运算)
t1 =np.arange(12).reshape(3,4)
# print(t1 + 1)
t2 = t1
print(t1 + t2)
print(t1)
t2 = np.arange(4).reshape(1,4)
print(t2)
print(t1 + t2)
# 矩阵的筛选 (同阶布尔矩阵)
print(t1[t1>8])

