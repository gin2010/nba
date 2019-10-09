import numpy as np

t1 = np.arange(12).reshape(3,4)
print(t1)
bool = np.array([False,
 True,
 False,
 ])

print(t1[bool])