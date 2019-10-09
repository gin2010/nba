# 编写工程下面的包路径即可
# import 包.模块路径 as 别名   通过别名获取模块里面的成员(变量、函数、类)
import day01_pm.demo01 as dd
# print(dd.a)
# dd.show()
# from .... import 成员
# 可以直接加载模块里面的成员,如果名称相同则就近原则
from day01_pm.demo01 import a,b,show as sh,Father

def show():
    print('========')

sh()
# 变量,系统的sum函数就被覆盖
# sum = 10
print(sum([1,2,3]))

import sys

for i in sys.path:
    print(i)