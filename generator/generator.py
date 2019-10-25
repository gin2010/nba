# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.1
# @Desc  :
import json,sys,os,time,random,copy
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator
from tool.search_dict import search_dict_key


class Generator_tjcx_kpcx(Generator):

    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        temp[inner_key] = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_tjcx_kpts(Generator):

    # 修改父类的模板
    # 统计查询接口--发票推送
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        try:
            temp = int(inner_value)
        except Exception:
            temp = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_fs(Generator):
    #
    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        temp = copy.deepcopy(temp)
        # 非税接口item只有“0006”与“0007”，zdyxmxx只有“0008”，head和jfxx都有
        # temp["head"]["djbm"] = random.choice(("0006", "0007", "0008"))
        # temp["head"]["djbm"] = random.choice(("0006", "0007"))
        temp["head"]["djbm"] = "0008"
        if temp["head"]["djbm"] == "0006":
            # 住院票据开立
            temp["head"]["mbdm"] = "0006"
            temp.pop("zdyxmxx",False)

        elif temp["head"]["djbm"] == "0007":
            # 门诊票据开立
            temp["head"]["mbdm"] = "0007"
            temp.pop("zdyxmxx", False)
        else:
            # 财政票据开立
            temp["head"]["mbdm"] = "0009"
            temp.pop("item", False)
        temp["head"]["pjdm"] = "24" + time.strftime("%y%m") + "000241"
        if inner_key == "pjhm":
            temp = search_dict_key(temp, inner_key, inner_value)
        else:
            # head等外层用
            # temp = search_dict_key(temp, inner_key, inner_value)
            # zdyxmxx里的zdyitems层使用
            temp["zdyxmxx"]["zdyitems"][0] = search_dict_key(temp["zdyxmxx"]["zdyitems"][0], inner_key, inner_value)
            # zdyxmxx里的xmbt层使用
            # temp["zdyxmxx"]["xmbt"] = search_dict_key(temp["zdyxmxx"]["xmbt"], inner_key, inner_value)
            temp["head"]["pjhm"] = int(fphm) + step
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
    #generate.generate_single_case()
    generate.generate_multiple_case()

