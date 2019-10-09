# -*- coding: utf-8 -*-
# @Date : 2019/09/29
# @Author : water
# @Version  : v1.0
# @Desc  :

import random

def generate_data1():
    # a + b > c 规则校验
    a = int()
    b = int()
    c = int()
    case = list()
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b > c:
            case.append([a,b,c,"T"])
            break
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b == c:
            case.append([a,b,c,"F"])
            break
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b < c:
            case.append([a,b,c,"F"])
            break
    return case


def generate_data(str):
    # a + b > c 规则校验
    a = int()
    b = int()
    c = int()
    case = list()
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b > c:
            case.append([a,b,c,"T"])
            break
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b == c:
            case.append([a,b,c,"F"])
            break
    while True:
        a = random.randint(1,100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        if a+b < c:
            case.append([a,b,c,"F"])
            break
    return case


def test_locals():
    # a = int()
    b = int()
    c = int()
    try:
        r = eval("a+b>c")
    except NameError as e:
        print(e.args)
    print(locals())

if __name__ == "__main__":
    # print(generate_data())
    test_locals()