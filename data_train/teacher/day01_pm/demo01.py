#  py 结尾的文件，称为模块: 变量、函数、类
# 除了类采用的是驼峰命名法，其它都是下划线
a = b = 100

def demo(x,y):
    return y,x

z1,z2 = demo(1,2)
print(z1,z2)


def show():
    print('show.......')


# 面向过程 ---> 面向对象
# name[]  age[]   tel[] ==> name[0]  age[0] tel[0]
# [{name:'张三',age:'28',tel:'183.....'},{},{},{....}]
class Father(object):
    # name  # 类属性
    # 双下划线开始和结束的方法称为特殊方法
    # 系统自动创建，而且一般自动调用，主要是实现某个特定功能
    # __init__ 对象初始化时自动被调用
    def __init__(self, name, age):
        print('__init__', self)
        # 对象属性
        self.name = name
        self.age = age

    # 一个下划线代表保护方法(自己，当前模块，子类)，两个下划线代表私有方法，
    # 只有类内部才能使用
    def show(self):
        print(f'name:{self.name},age:{self.age}')


# 双下划线开始和结束的变量称为特殊变量
if __name__ == "__main__":
    # 创建对象时自动会init方法
    # self就是java this,代表当前对象,系统会自动传入
    f = Father('张三', 19)
    f.show()
