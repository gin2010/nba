# -*- coding: utf-8 -*-
# @Date : 2019/09/16
# @Author : water
# @Desc  : 根据传入的sort列表中数据类型及总长度length，生成sort中每种数据类型的长度，合计长度=length
# @Version  : v0.1

import random

def random_count(sort,length):
    if length ==len(sort):
        sort_count = dict()
        for i in range(len(sort)):
            sort_count[sort[i]] = 1
        return sort_count
    else:
        while True:
            sort_count = dict()
            for i in range(len(sort)-1):
                sort_count[sort[i]] = random.randint(1,length-len(sort))
            sort_count[sort[len(sort)-1]] = length - sum(sort_count.values())
            if sort_count[sort[len(sort)-1]] > 1 :
                break
        return sort_count


if __name__=="__main__":
    sort_count = random_count(["SZ","ZMX","ZMD","FT","NT"],100)
    print(sort_count)
    if sum(sort_count.values())==100:
        print("right!!!")
    # 测试length=1的情况
    sort_count = random_count(["SZ"], 1)
    print(sort_count)
    # 测试length=2的情况
    sort_count = random_count(["SZ"], 2)
    print(sort_count)
    # 测试length=2的情况
    sort_count = random_count(["SZ","ZMD"], 2)
    print(sort_count)
    # 测试length=3的情况
    sort_count = random_count(["SZ","ZMX","ZMD"], 3)
    print(sort_count)
    # 测试length=3的情况
    sort_count = random_count(["SZ","ZMD"], 3)
    print(sort_count)