# 导入科学库
import numpy as np
# 一维矩阵的创建  numpy.ndarray
t1 = np.arange(12)
# (12,)  一维矩阵,有12个元素
print(t1,type(t1),t1.shape)
print(t1.dtype,t1.size)
print('创建二维矩阵.........')
t1 = np.arange(12).reshape(3,4)
print(t1,type(t1),t1.shape)
print(t1.dtype,t1.size)
print('创建不同数据类型的二维矩阵')
t1 = np.array([[1,2,True],
          [100,200,False],
          ['1','2',3]
          ])
print(t1,type(t1),t1.shape)
print(t1.dtype,t1.size)
