# -*- coding: utf-8 -*-
# @Date : 2019/09/20
# @Author : water
# @Version  : v1.0
# @Desc  :从51核心的用例模板导入到51发票采集自动化用例中

import os,xlrd,json,copy,time
import logging
from tool.operateMysqlClass import OperateMysql

#日志配置
logging.basicConfig(level=logging.DEBUG,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 常量
FPKJ_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","fpzf_case.xls")
TEMPLATE_SINGLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "template_single.temp")
with open(TEMPLATE_SINGLE_PATH, 'r') as f:
    TEMPLATE_SINGLE = json.load(f)
    # logger.info(TEMPLATE_SINGLE)


# 读取51核心导出来的excel测试用例
def read_excel_load_case(path):
    wb = xlrd.open_workbook(path)
    ws_fpkj = wb.sheet_by_name("fpkj")
    max_row = ws_fpkj.nrows
    logger.info(max_row)
    case_load_list = list()  # 列表里存放excel列名：每行数据组成的字典
    for r in range(1, max_row):
        l = list()
        request_name = ws_fpkj.cell(r, 0).value + ws_fpkj.cell(r,1).value
        l.append(request_name)
        l.append(ws_fpkj.cell(r, 3).value)
        case_load_list.append(l)
    logger.info(case_load_list[0])
    ws_common = wb.sheet_by_name("common")
    commons_dict = dict()
    commons_dict["case_id"] = ws_common.cell(0, 1).value
    commons_dict["http_method"] = ws_common.cell(1, 1).value
    commons_dict["url_sql"] = ws_common.cell(2, 1).value
    commons_dict["step"] = ws_common.cell(3, 1).value
    commons_dict["test_desc"] = ws_common.cell(4, 1).value
    commons_dict["out_put"] = ws_common.cell(5, 1).value
    commons_dict["fphm"] = ws_common.cell(6, 1).value
    logger.info(commons_dict)
    return case_load_list,commons_dict


# 根据51核心的请求报文更新template里对应的值
def update_template(data,temp=TEMPLATE_SINGLE):
    temp_kj = temp["FPXX"]["FP_KJ"]    #发票头信息（dict）
    # temp_wl = temp["FPXX"]["FP_WLXX"]  #发票物流信息（dict）
    # temp_zf = temp["FPXX"]["FP_ZFXX"]  #发票支付信息（dict）
    # data 是核心的模板数据
    # 更新发票主信息
    data_kj = data["FPKJXX_FPTXX"]  #发票头信息（dict）
    if data_kj.get("FPQQLSH") is not None:
        temp_kj["FPQQLSH"] = data_kj["FPQQLSH"]   #发票请求流水号

    if data_kj.get("XHFMC") is not None:
        temp_kj['XSF_NSRMC'] = data_kj['XHFMC']  # 销货方纳税人名称

    if data_kj.get("XHF_NSRSBH") is not None:
        temp_kj['XSF_NSRSBH'] = data_kj['XHF_NSRSBH']  # 销货方纳税人识别号

    if data_kj.get("KPRQ") is not None:
        temp_kj['KPRQ'] = data_kj['KPRQ']  # 开票日期

    if data_kj.get("KPLX") is not None:
        temp_kj['KPLX'] = data_kj['KPLX']  # 开票类型

    if data_kj.get("KPHJJE") is not None:
        temp_kj['KPHJJE'] = data_kj['KPHJJE']  # 开票合计金额

    if data_kj.get("HJBHSJE") is not None:
        temp_kj['HJBHSJE'] = data_kj['HJBHSJE']  # 合计不含税金额

    if data_kj.get("HJSE") is not None:
        temp_kj['KPHJSE'] = data_kj['HJSE']  # 开票合计税额

    if data_kj.get("KPXM") is not None:
        temp_kj['KPXM'] = data_kj['KPXM']  # 开票项目

    if data_kj.get("GHF_NSRSBH") is not None:
        temp_kj['GMF_NSRSBH'] = data_kj['GHF_NSRSBH']  # 购货方纳税人识别号

    if data_kj.get("GHFMC") is not None:
        temp_kj['GMF_NSRMC'] = data_kj['GHFMC']  # 购货方纳税人名称

    if data_kj.get("GHF_YHZH") is not None:
        temp_kj['GMF_YHZH'] = data_kj['GHF_YHZH']  # 购货方银行账号

    if data_kj.get("GHF_DZDH") is not None:
        temp_kj['GMF_DZ'] = data_kj['GHF_DZDH']  # 购货方地址

    if data_kj.get("GHF_SJ") is not None:
        temp_kj['GMF_SJ'] = data_kj['GHF_SJ']  # 购货方手机

    if data_kj.get("GHF_EMAIL") is not None:
        temp_kj['GMF_EMAIL'] = data_kj['GHF_EMAIL']  # 购货方邮箱

    if data_kj.get("YFP_HM") is not None:
        temp_kj['YFPHM'] = data_kj['YFP_HM']  # 原发票号码

    if data_kj.get("YFP_DM") is not None:
        temp_kj['YFPDM'] = data_kj['YFP_DM']  # 原发票代码

    if data_kj.get("KPY") is not None:
        temp_kj['KPY'] = data_kj['KPY']  # 开票员

    if data_kj.get("SKY") is not None:
        temp_kj['SKY'] = data_kj['SKY']  # 收款员

    if data_kj.get("FHR") is not None:
        temp_kj['FHR'] = data_kj['FHR']  # 复核人

    if data_kj.get("SWJG_DM") is not None:
        temp_kj['SWJG_DM'] = data_kj['SWJG_DM']  # 税务机构代码

    if data_kj.get("FPZL_DM") is not None:
        temp_kj['FP_ZLDM'] = data_kj['FPZL_DM']  # 发票种类代码

    if data_kj.get("XHF_DZDH") is not None:
        temp_kj['XSF_DZ'] = data_kj['XHF_DZDH']  # 销售方地址

    if data_kj.get("XHF_YHZH") is not None:
        temp_kj['XSF_YHZH'] = data_kj['XHF_YHZH']  # 销售方银行账号

    if data_kj.get("FJH") is not None:
        temp_kj['FJH'] = data_kj['FJH']  # 分机号

    if data_kj.get("DKBZ") is not None:
        temp_kj['DKBZ'] = data_kj['DKBZ']  # 代开标志

    if data_kj.get("TSCHBZ") is not None:
        temp_kj['TSCHBZ'] = data_kj['TSCHBZ']  # 特殊冲红标志

    if data_kj.get("CHYY") is not None:
        temp_kj['CHYY'] = data_kj['CHYY']  # 冲红原因

    if data_kj.get("BMB_BBH") is not None:
        temp_kj['BMB_BBH'] = data_kj['BMB_BBH']  # 编码表版本号

    if data_kj.get("QD_BZ") is not None:
        temp_kj['QD_BZ'] = data_kj['QD_BZ']  # 清单标志

    if data_kj.get("DDH") is not None:
        temp_kj['DDH'] = data_kj['DDH']  # 订单号

    if data_kj.get("SGBZ") is not None:
        temp_kj['SGBZ'] = data_kj['SGBZ']  # 收购标志

    if data_kj.get("BZ") is not None:
        temp_kj['BZ'] = data_kj['BZ']  # 备注

    # if data_kj.get("BYZD1") is not None:
    #     temp_kj['BYZD1'] = data_kj['BYZD1']  # 备用字段1
    #
    # if data_kj.get("BYZD2") is not None:
    #     temp_kj['BYZD2'] = data_kj['BYZD2']  # 备用字段2
    #
    # if data_kj.get("BYZD3") is not None:
    #     temp_kj['BYZD3'] = data_kj['BYZD3']  # 备用字段3
    #
    # if data_kj.get("BYZD4") is not None:
    #     temp_kj['BYZD4'] = data_kj['BYZD4']  # 备用字段4
    #
    # if data_kj.get("BYZD5") is not None:
    #     temp_kj['BYZD5'] = data_kj['BYZD5']  # 备用字段5

    # 更新发票明细信息，如果多行明细需要添加
    data_mx = data["FPKJXX_XMXXS"]  #明细信息（list）
    mx_count = len(data_mx)  #明细共有几条
    result_mx = list()
    for i in range(mx_count):
        temp_mx = copy.deepcopy(temp["FPXX"]["FP_KJ_MX"][0])  # 取模板第一条明细数据（dict）
        temp_mx["SPHXH"] = i + 1
        if data_mx[i].get("XMMC") is not None:
            temp_mx["SPMC"] = data_mx[i]["XMMC"]    # 商品名称

        if data_mx[i].get("XMSL") is not None:
            temp_mx['SPSL'] = data_mx[i]['XMSL']  # 商品数量

        if data_mx[i].get("XMJE") is not None:
            temp_mx['SPJE'] = data_mx[i]['XMJE']  # 商品金额

        if data_mx[i].get("XMDJ") is not None:
            temp_mx['SPDJ'] = data_mx[i]['XMDJ']  # 商品单价

        if data_mx[i].get("XMDW") is not None:
            temp_mx['DW'] = data_mx[i]['XMDW']  # 单位

        if data_mx[i].get("GGXH") is not None:
            temp_mx['GGXH'] = data_mx[i]['GGXH']  # 规格型号

        if data_mx[i].get("HSBZ") is not None:
            temp_mx['HSJBZ'] = data_mx[i]['HSBZ']  # 含税价标志

        if data_mx[i].get("KCE") is not None:
            temp_mx['KCE'] = data_mx[i]['KCE']  # 扣除额

        if data_mx[i].get("SE") is not None:
            temp_mx['SE'] = data_mx[i]['SE']  # 税额

        if data_mx[i].get("SL") is not None:
            temp_mx['SL'] = data_mx[i]['SL']  # 税率

        if data_mx[i].get("SPBM") is not None:
            temp_mx['SPBM'] = data_mx[i]['SPBM']  # 商品编码

        if data_mx[i].get("ZXBM") is not None:
            temp_mx['ZXBM'] = data_mx[i]['ZXBM']  # 自行编码

        if data_mx[i].get("YHZCBS") is not None:
            temp_mx['YHZCBS'] = data_mx[i]['YHZCBS']  # 优惠政策标识

        if data_mx[i].get("LSLBS") is not None:
            temp_mx['LSLBS'] = data_mx[i]['LSLBS']  # 零税率标识

        if data_mx[i].get("ZZSTSGL") is not None:
            temp_mx['ZZSTSGL'] = data_mx[i]['ZZSTSGL']  # 增值税特殊管理

        if data_mx[i].get("FPHXZ") is not None:
            temp_mx['FPHXZ'] = data_mx[i]['FPHXZ']  # 发票行性质
        result_mx.append(temp_mx)
        # if data_mx[i].get("BYZD1") is not None:
        #     temp_mx['BYZD1'] = data_mx[i]['BYZD1']  # 备用字段1
        # if data_mx[i].get("BYZD2") is not None:
        #     temp_mx['BYZD2'] = data_mx[i]['BYZD2']  # 备用字段2
        # if data_mx[i].get("BYZD3") is not None:
        #     temp_mx['BYZD3'] = data_mx[i]['BYZD3']  # 备用字段3
        # if data_mx[i].get("BYZD4") is not None:
        #     temp_mx['BYZD4'] = data_mx[i]['BYZD4']  # 备用字段4
        # if data_mx[i].get("BYZD5") is not None:
        #     temp_mx['BYZD5'] = data_mx[i]['BYZD5']  # 备用字段5
    temp["FPXX"]["FP_KJ_MX"].clear()
    temp["FPXX"]["FP_KJ_MX"] = result_mx
    return temp

# 导入用例主函数
def generate_load_case_main():
    datas,commons = read_excel_load_case(FPKJ_PATH)
    # logger.info(datas[0]) #测试语句，可删除
    # temp = update_template(eval(datas[0][1])) #测试语句，可删除
    opsql = OperateMysql()
    for data in datas:
        temp = update_template(eval(data[1]))
        commons["step"] = int(commons["step"]) + 1
        # 修改模板中发票代码
        temp['FPXX']['FP_KJ']['FPDM'] = "24" + time.strftime("%y%m") + "000240"
        # 修改模板中发票号码
        temp['FPXX']['FP_KJ']['FPHM'] = int(commons["fphm"]) + int(commons["step"])
        commons["request_name"] = data[0]
        commons["request_sql_param"] = json.dumps(temp,ensure_ascii=False)
        logger.info(commons)
        opsql.insert_sql(commons)
    opsql.close()
    logger.warning("------ end ------！")


if __name__ == "__main__":
    generate_load_case_main()
