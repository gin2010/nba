# -*- coding: utf-8 -*-
# File  : 01-basic1.py
# Author: water
# Date  : 2019/7/31

for i in range(1,4):
    email = input ('email:')
    index = email.find("@")
    if index>0:
        name = email[:index]
        email_sort = email[index+1:]
        print(f'邮箱名：{name}  类型：{email_sort}')
        break
    else:
        print("input wrong")
else:
    print(f"输入{i}次错误，锁定")