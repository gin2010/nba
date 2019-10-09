# -*- coding: utf-8 -*-
# @Date : 2019/09/23
# @Author : water
# @Version  : v1.0
# @Desc  : 学习csv模块，学习类的使用、模块


class PersonClass:

    def __init__(self,name):
        self._name = name
        self._print_name()


    def _print_name(self):
        print("my name is :{}".format(self._name))


class StudentClass1(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score


class StudentClass2(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    def get_score(self):
        return self.__score
    def set_score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score


class StudentClass3(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    @property
    def score(self):
        """get方法"""
        return self.__score
    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score


class StudentClass4(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score

    def get_score(self):
        """get方法"""
        return self.__score

    def set_score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

    score = property(get_score,set_score)


if __name__ == "__main__":
    # xiaoming = PersonClass("xiaoming")

    # #st1可以使用点来访问私有变量
    # st1 = StudentClass1('xiaobai',50)
    # print(st1.score)
    # st1.score=100
    # print(st1.score)

    # #st2无法使用点来访问私有变量
    # st2 = StudentClass2('xiaoxin',70)
    # print(st2.get_score())
    # st2.set_score(90)
    # print(st2.get_score())

    # # 经过property装修后，可以使用点来访问
    # st3 = StudentClass3('xiaoxin',70)
    # print(st3.score)
    # st3.score =99
    # print(st3.score)

    # 经过property()函数，可以使用点来访问
    st4 = StudentClass4('xiaoxin',70)
    print(st4.score)
    st4.score =99
    print(st4.score)

