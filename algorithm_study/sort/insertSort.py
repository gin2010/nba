# -*- coding: utf-8 -*-
# @Date : 2019/10/09
# @Author : water
# @Version  : v1.0
# @Desc  : 插入排序算法实现

import os

def insert_sort(l):
    '''
    插入排序算法（升序）：从列表中第二个元素开始，与前面的元素比较，
    如果比前面的元素小则插入到该元素的位置中。
    :param l: 待排序的列表
    :return: 排序后的列表
    '''
    for i in range(1,len(l)):
        target = l[i]
        for j in range(i-1,-1,-1):
            if target < l[j]:    #只需要将这个小于号变成大于号就可以实现降序
                l[j+1] = l[j]
                l[j] = target
    return l


def insert_sort2(l,default=True):
    '''
    插入排序算法（升序）：从列表中第二个元素开始，与前面的元素比较，
    如果比前面的元素小则插入到该元素的位置中。
    :param l: 待排序的列表
    :return: 排序后的列表
    '''
    if default==True:
        flag = "target < l[j]"
    else:
        flag = "target > l[j]"
    for i in range(1,len(l)):
        target = l[i]
        for j in range(i-1,-1,-1):
            if eval(flag):    #只需要将这个小于号变成大于号就可以实现降序
                l[j+1] = l[j]
                l[j] = target
    return l

def insert_sort3(l,singal="<"):
    '''
    插入排序算法（升序）：从列表中第二个元素开始，与前面的元素比较，
    如果比前面的元素小则插入到该元素的位置中。
    提取出运算符作为参数来传递
    :param l: 待排序的列表
    :return: 排序后的列表
    '''

    flag = "target {} l[j]".format(singal)
    for i in range(1,len(l)):
        target = l[i]
        for j in range(i-1,-1,-1):
            if eval(flag):    #只需要将这个小于号变成大于号就可以实现降序
                l[j+1] = l[j]
                l[j] = target
    return l

if __name__ == "__main__":
    l = insert_sort3([6,7,5,3,9,4,1,2],">")
    print(l)