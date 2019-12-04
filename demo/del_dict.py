# -*- coding: utf-8 -*-
# @Date : 2019/10/21
# @Author : water
# @Version  : v1.0
# @Desc  :

d = {"a":1,"b":2,"c":{"c1":11,"c2":12}}
print(d.pop("c",False)) #删除字典d中的"c"，如果不存在这个Key，就返回False
print(d)
print(d.pop("dd",False))