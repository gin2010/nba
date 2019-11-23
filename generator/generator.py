# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.2
# @Desc  :每次改写update_temp_single方法，更改最终传入到request_sql_param中内层报文的内容，由于不同的接口内层报文不一致，
#         因此将此方法针对不同的接口报文类型**重写**，不同的接口通过修改配置文件中模板文件temp与模板类型
#         发票采集模板使用：
#         1修改发票号码、发票代码；
#         2将内层报文参数inner_param的值修改为inner_param_value并返回
#         :param temp:内层报文（从模板文件中读取的）
#         :param step:测试用例step（从excel模板common中读取的step）
#         :param fphm:发票号码（从excel模板common中读取的起始发票号码）
#         :param inner_key:内层报文中需要更新的key（从excel模板case中读取的每一行request_param的值），相当于每次修改的字段
#         :param inner_value:内层报文中需要更新的key对应的value（GetString返回的字段值，一次传入一个）
#         :return temp: 转换为json格式的内层报文，写入到数据库request_sql_param的内容


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
        temp["head"]["djbm"] = random.choice(("0006", "0007", "0008"))
        # temp["head"]["djbm"] = random.choice(("0006", "0007"))
        # temp["head"]["djbm"] = "0008"
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
            temp = search_dict_key(temp, inner_key, inner_value)
            # zdyxmxx里的zdyitems层使用
            # temp["zdyxmxx"]["zdyitems"][0] = search_dict_key(temp["zdyxmxx"]["zdyitems"][0], inner_key, inner_value)
            # zdyxmxx里的xmbt层使用
            # temp["zdyxmxx"]["xmbt"] = search_dict_key(temp["zdyxmxx"]["xmbt"], inner_key, inner_value)
            temp["head"]["pjhm"] = int(fphm) + step
        return json.dumps(temp, ensure_ascii=False)


class Generator_ys_tbqyxx(Generator):

    # 修改父类的模板
    # 51云税--客户信息查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        try:
            temp = search_dict_key(temp, inner_key, inner_value)
        except Exception:
            os.exit(0)
            self.logger.error("inner_key:{} not found".format(inner_value))
        return json.dumps(temp, ensure_ascii=False)


    # 修改父类的update_temp_multiple方法
    def update_temp_multiple(self,temp,step,fphm,inner_keys,inner_values):
        temp1 = copy.deepcopy(temp)
        for i in range(len(inner_keys)):
            temp1 = search_dict_key(temp1, inner_keys[i], inner_values[i])
        return json.dumps(temp1, ensure_ascii=False)

if __name__ == "__main__":
    # 统计查询接口--开票查询
    # generate = Generator_tjcx_kpcx()
    # generate.generate_single_case()

    # 统计查询接口--发票推送
    # generate = Generator_tjcx_kpts()
    # generate.generate_single_case()

    # 非税接口
    # generate = Generator_fs()
    # generate.generate_single_case()  # 生成单个字段的用例
    # generate.generate_multiple_case()  # 生成多字段用例

    # 51云税 信息查询
    generate = Generator_ys_tbqyxx()
    # generate.generate_single_case()  # 生成单个字段的用例
    generate.generate_multiple_case()  # 生成多字段用例

