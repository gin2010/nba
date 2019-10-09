# -*- coding: utf-8 -*-
# File  : class_demo.py
# Author: water
# Date  : 2019/7/31
aa = 111

def show():
    print('show.....')

class Father(object):

    # 类属性
    class_name = 'father'

    def __init__(self,name,age):
        print('__init__',self)
        #对象属性
        self.name = name
        self.age = age

    def show(self):
        print(self.name,"---",self.age)




if __name__=="__main__":

    f1 = Father('xiaobai',19)
    print("print",f1,id(f1))
    f1.show()