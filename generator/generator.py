# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.1
# @Desc  :
import json,sys,os
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator



class Generator_tjcx_kpcx(Generator):

    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp方法
    def update_temp(self,temp,step,fphm,inner_key,inner_value):
        temp[inner_key] = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_tjcx_kpts(Generator):

    # 修改父类的模板
    # 统计查询接口--发票推送
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp方法
    def update_temp(self,temp,step,fphm,inner_key,inner_value):
        try:
            temp = int(inner_value)
        except Exception:
            temp = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_fs(Generator):

    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp方法
    def update_temp(self,temp,step,fphm,inner_key,inner_value):
        temp[inner_key] = inner_value
        return json.dumps(temp, ensure_ascii=False)



if __name__ == "__main__":
    # 统计查询接口--开票查询
    # generate = Generator_tjcx_kpcx()
    # generate.generate_single_case()

    # 统计查询接口--发票推送
    # generate = Generator_tjcx_kpts()
    # generate.generate_single_case()

    # 非税接口
    generate = Generator_fs()
    generate.generate_single_case()

