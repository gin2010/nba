# -*- coding: utf-8 -*-
# @Date : 2019-8-28
# @Author : water
# @Desc  :实现传入字符类型与长度，返回固定长度的字符
# @Version  : v0.1

"""
{"字母":"A",
"数字":"D",
"汉字":"C",
"汉字+字母":"CA",
"字母+数字":"AD",
"汉字+数字":"CD",
"汉字+数字+字母":"CDA",
"特殊符号":"S",
"空":"B",
"难繁体字":"F",
"全角数字":"SBC",
"小数":"DB",
"日期":"DT",
}
"""

import random
import string
import os
random.randint(1,360)

#prepare for data

ALPHABETS = string.ascii_letters
DIGITS = string.digits
FILEPATH = os.path.dirname(os.path.abspath(__file__))
def GBK2312():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)   # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    chinese = bytes.fromhex(val).decode('gb2312')
    return chinese_common

f = open(os.path.join(FILEPATH,"config","commonChinese.txt"),encoding='utf-8')
chinese_common = f.readline().split(sep=',')
print(chinese_common)
print(type(chinese_common))
print(chinese_common[1])