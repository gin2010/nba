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



class Generator_tjcx(Generator):

    # 修改父类的模板
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp方法
    def update_temp(self,temp,step,fphm,inner_key,inner_value):
        temp[inner_key] = inner_value
        return json.dumps(temp, ensure_ascii=False)


if __name__ == "__main__":
    print(sys.path)
    generate = Generator_tjcx()
    generate.generate_single_case()