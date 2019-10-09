# -*- coding: utf-8 -*-
# @Date : 2019-9-18
# @Author : water
# @Desc  :
# @Version  : v1.1 增加char_case中“生成值为0或1或2”的情况，因为大多数char类型的值都是0，1 ，2


import logging
import copy
import os,math,json,xlrd,time
from tool.operateMysqlClass import OperateMysql
from tool.randomString import GetString
# 查看变量的装修器
import pysnooper as ps

# 程序运行日志配置
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEMPLATE_MULTIPLE = {}
TEMPLATE_SINGLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "template_single.temp")
with open(TEMPLATE_SINGLE_PATH, 'r') as f:
    TEMPLATE_SINGLE = json.load(f)
    logger.info(TEMPLATE_SINGLE)
EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cases.xls")

def read_xls_multiple(path):
    # 读取cases.xls表common sheet中的case_id,http_method等每个用例中固定的值，组成字典
    # 读取cases.xls表中case sheet中的step,request_param等每个用例中变化的值，组成如下类型的字典
    '''
    {
        'step': '5555',
        'test_desc': '发票代码10位、发票号码8位',
        'request': {
            'fp_dm': '1234567890',
            'fp_hm': '12345678'
        }
    }
    '''
    commons_dict = dict()
    case_list = list()
    wb = xlrd.open_workbook(path)
    ws_common = wb.sheet_by_name("common")
    ws_case = wb.sheet_by_name("case")
    max_row_common = ws_common.nrows
    for r in range(max_row_common):
        commons_dict[ws_common.cell(r, 0).value] = ws_common.cell(r, 1).value
    logger.info(max_row_common)
    logger.info(commons_dict)
    max_row_case = ws_case.nrows
    logger.info(max_row_case)
    for r in range(1, max_row_case):
        d = dict()
        d['step'] = ws_case.cell(r, 0).value
        d['test_desc'] = ws_case.cell(r, 1).value
        d['out_put'] = ws_case.cell(r, 2).value
        request_param = ws_case.cell(r, 3).value.strip().split(sep="\n")
        request_value = ws_case.cell(r, 4).value.strip().split(sep="\n")
        if request_param != [""]:
            request_dict = dict(zip(request_param, request_value))
            d['request'] = request_dict
        else:
            d['request'] = ""
        case_list.append(d)
    logger.info(case_list)
    return commons_dict, case_list
    pass

# 使用excel里通用数据更新template里的数据
# @ps.snoop()
def modify_template_multiple(commons_dict, case_list, template):
    """
    生成如下格式的数据库内容(content_dict)
    {'case_id': '99999',
    'http_method': 'post',
    'url_sql': '/deliver/deliver'
    'step': '11111',
    'test_desc': '导入参数',
    'out_put': {"51KEY":"22793094"},
    'request': {
        "fp_dm": "114015117001",
        "fp_hm": "64879681",
        "gmf_mc": "航天信息",
        "gmf_nsrsbh": "123666",
        ....
        "xsf_nsrsbh": "140301197609244968"
        }
    }
    """
    contents_list = list()
    for d in case_list:
        content_dict = dict()
        content_dict.update(commons_dict)
        if d['request'] != "":
            template.update(d['request'])
        d['request'] = template
        content_dict.update(d)
        logger.info("-" * 10, content_dict)
        contents_list.append(content_dict)
        logger.info("----content_list:", contents_list)
    logger.info(contents_list)
    return contents_list
    pass

# 生成多字段用例主函数
def generate_multiple_case_main(path=EXCEL_PATH, ):
    # 读取excel
    commons_dict, case_list = read_xls(path)
    # 以excel中的数据更新template里的数据
    contents_list = modify_template_multiple(commons_dict, case_list, TEMPLATE_MULTIPLE)
    # 连接数据库
    opsql = OperateMysql()
    opsql.insert_sql(data)
    opsql.close()
    pass


# 读取case_single.xls里的用例
def read_xls_single():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "case_single.xls")
    wb = xlrd.open_workbook(path)
    ws_case = wb.sheet_by_name("case")
    max_row_case = ws_case.nrows
    case_single_list = list()   # 列表里存放excel列名：每行数据组成的字典
    for r in range(1, max_row_case):
        d = dict()
        d['resquest_param'] = ws_case.cell(r, 0).value
        d['param_sort'] = ws_case.cell(r, 1).value
        d['length'] = ws_case.cell(r, 2).value
        case_single_list.append(d)
    logger.info(case_single_list)
    ws_common = wb.sheet_by_name("common")
    commons_dict = dict()
    commons_dict["case_id"] = ws_common.cell(0,1).value
    commons_dict["http_method"] = ws_common.cell(1,1).value
    commons_dict["url_sql"] = ws_common.cell(2,1).value
    commons_dict["step"] = ws_common.cell(3,1).value
    commons_dict["test_desc"] = ws_common.cell(4,1).value
    commons_dict["out_put"] = ws_common.cell(5,1).value
    commons_dict["fphm"] = ws_common.cell(6, 1).value
    logger.info(commons_dict)
    return case_single_list,commons_dict


# 生成VARCHAR的通用测试用例
def varchar_case(length):
    length = int(length)
    results = list()
    getstring = GetString()
    # 1生成length位的数字
    results.append([f"生成{length}位的数字T", getstring.random_string_multiple(['SZ'], length)])
    # 2生成length+1位的数字
    results.append([f"生成{length+1}位的数字F", getstring.random_string_multiple(['SZ'], length + 1)])
    # 3生成length位的数字（两边有空格）
    results.append([f"生成{length}位的数字（两边有空格）T", "   " + getstring.random_string_multiple(['SZ'], length) + "  "])
    # 4生成length位的数字（中间有空格）
    results.append([f"生成{length}位的数字（中间有空格）F", getstring.random_string_multiple(['SZ'], length)[:math.floor(length/2)] + "   "+ getstring.random_string_multiple(['SZ'], length)[math.floor(length/2):length]])
    # 5生成length位的大写字母
    results.append([f"生成{length}位的大写字母T", getstring.random_string_multiple(['ZMD'], length)])
    # 6生成length+1位的大写字母
    results.append([f"生成{length+1}位的大写字母F", getstring.random_string_multiple(['ZMD'], length + 1)])
    # 7生成length位的小写字母
    results.append([f"生成{length}位的小写字母T", getstring.random_string_multiple(['ZMX'], length)])
    # 8生成length+1位的小写字母
    results.append([f"生成{length+1}位的小写字母F", getstring.random_string_multiple(['ZMX'], length + 1)])
    # 9生成length位的小写字母、数字
    if length >= 2:
        results.append([f"生成{length}位的小写字母、数字T", getstring.random_string_multiple(['ZMX', 'SZ'], length)])
    # 10生成length+1位的小写字母、数字
    if length+1 >= 2:
        results.append([f"生成{length+1}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length + 1)])
    # 11生成length位大写字母、数字
    if length >= 2:
        results.append([f"生成{length}位大写字母、数字T", getstring.random_string_multiple(['ZMD', 'SZ'], length)])
    # 12生成length+1位大写字母、数字
    if length+1 >= 2:
        results.append([f"生成{length+1}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length + 1)])
    # 13生成length位大小写字母、数字
    if length >= 3:
        results.append([f"生成{length}位大小写字母、数字T", getstring.random_string_multiple(['ZMD', 'ZMX', 'SZ'], length)])
    # 14生成length位全角数字
    results.append([f"生成{length}位全角数字F", getstring.random_string_multiple(['QJSZ'], length)])
    # 15生成length位大小写字母
    if length >= 2:
        results.append([f"生成{length}位大小写字母T", getstring.random_string_multiple(['ZMD', 'ZMX'], length)])
    # 16生成length位的汉字
    results.append([f"生成{length}位的汉字T", getstring.random_string_multiple(['HZ'], length)])
    # 17生成length+1位的汉字
    results.append([f"生成{length+1}位的汉字F", getstring.random_string_multiple(['HZ'], length + 1)])
    # 18生成length位的繁体字
    results.append([f"生成{length}位的繁体字T", getstring.random_string_multiple(['FT'], length)])
    # 19生成length位的难体字
    results.append([f"生成{length}位的难体字T", getstring.random_string_multiple(['NT'], length)])
    # 20生成length位的特殊符号
    results.append([f"生成{length}位的特殊符号T", getstring.random_string_multiple(['FH'], length)])
    # 21生成空值
    results.append(["生成空值F",''])
    # 22生成null值
    results.append(["生成null值F",'null'])
    # 23sql注入 "or"1"="1
    results.append(["sql注入F",getstring.random_string_multiple(['SZ'], length) + "''or''1''=''1"])
    # 24生成length-1位的数字
    if length-1>=1:
        results.append([f"生成{length-1}位的数字T", getstring.random_string_multiple(['SZ'], length-1)])
    # 25生成length-1位的大写字母
    if length-1>=1:
        results.append([f"生成{length-1}位的大写字母F", getstring.random_string_multiple(['ZMD'], length-1)])
    # 26生成length-1位的小写字母
    if length-1>=1:
        results.append([f"生成{length-1}位的小写字母F", getstring.random_string_multiple(['ZMX'], length-1)])
    logger.info(results)
    return results


# 生成INT的通用测试用例
def char_case(length):
    length = int(length)
    results = list()
    getstring = GetString()
    # 1生成length位的数字
    results.append([f"生成{length}位的数字T", getstring.random_string_multiple(['SZ'], length)])
    # 2生成length+1位的数字
    results.append([f"生成{length+1}位的数字F", getstring.random_string_multiple(['SZ'], length + 1)])
    # 3生成length位的数字（两边有空格）
    results.append([f"生成{length}位的数字（两边有空格）F", "   " + getstring.random_string_multiple(['SZ'], length) + "  "])
    # 4生成length位的数字（中间有空格）
    results.append([f"生成{length}位的数字（中间有空格）F", getstring.random_string_multiple(['SZ'], length)[:math.floor(length / 2)] + "   " + getstring.random_string_multiple(['SZ'], length)[math.floor(length / 2):length]])
    # 5生成length位的大写字母
    results.append([f"生成{length}位的大写字母T", getstring.random_string_multiple(['ZMD'], length)])
    # 6生成length+1位的大写字母
    results.append([f"生成{length+1}位的大写字母F", getstring.random_string_multiple(['ZMD'], length + 1)])
    # 7生成length位的小写字母
    results.append([f"生成{length}位的小写字母F", getstring.random_string_multiple(['ZMX'], length)])
    # 8生成length+1位的小写字母
    results.append([f"生成{length+1}位的小写字母F", getstring.random_string_multiple(['ZMX'], length + 1)])
    # 9生成length位的小写字母、数字
    if length >= 2:
        results.append([f"生成{length}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length)])
    # 10生成length+1位的小写字母、数字
    if length+1 >= 2:
        results.append([f"生成{length+1}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length + 1)])
    # 11生成length位大写字母、数字
    if length >= 2:
        results.append([f"生成{length}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length)])
    # 12生成length+1位大写字母、数字
    if length+1 >= 2:
        results.append([f"生成{length+1}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length + 1)])
    # 13生成length位大小写字母、数字
    if length >= 3:
        results.append([f"生成{length}位大小写字母、数字F", getstring.random_string_multiple(['ZMD', 'ZMX', 'SZ'], length)])
    # 14生成length位全角数字
    results.append([f"生成{length}位全角数字F", getstring.random_string_multiple(['QJSZ'], length)])
    # 15生成length位大小写字母
    if length >= 2:
        results.append([f"生成{length}位大小写字母F", getstring.random_string_multiple(['ZMD', 'ZMX'], length)])
    # 16生成length位的汉字
    results.append([f"生成{length}位的汉字F", getstring.random_string_multiple(['HZ'], length)])
    # 17生成length+1位的汉字
    results.append([f"生成{length+1}位的汉字F", getstring.random_string_multiple(['HZ'], length + 1)])
    # 18生成length位的繁体字
    results.append([f"生成{length}位的繁体字F", getstring.random_string_multiple(['FT'], length)])
    # 19生成length位的难体字
    results.append([f"生成{length}位的难体字F", getstring.random_string_multiple(['NT'], length)])
    # 20生成length位的特殊符号
    results.append([f"生成{length}位的特殊符号F", getstring.random_string_multiple(['FH'], length)])
    # 21生成空值
    results.append(["生成空值F", ''])
    # 22生成null值
    results.append(["生成null值F", 'null'])
    # 23sql注入 "or"1"="1
    results.append(["sql注入F", getstring.random_string_multiple(['SZ'], length) + "''or''1''=''1"])
    # 24超长位数数字
    results.append([f"生成超长位数数字T", getstring.random_string_multiple(['SZ'], length+length)])
    # 25值为0
    results.append([f"值为0T", '0'])
    # 26值为1
    results.append([f"值为1T", '1'])
    # 27值为2
    results.append([f"值为2T", '2'])
    # 28生成length-1位的数字
    if length-1 >= 1:
        results.append([f"生成{length-1}位的数字F", getstring.random_string_multiple(['SZ'], length - 1)])
    # 29生成length-1位的大写字母
    if length-1 >= 1:
        results.append([f"生成{length-1}位的大写字母F", getstring.random_string_multiple(['ZMD'], length - 1)])
    # 30生成length-1位的小写字母
    if length - 1 >= 1:
        results.append([f"生成{length-1}位的小写字母F", getstring.random_string_multiple(['ZMX'], length - 1)])
    logger.debug(results)
    return results


# 生成DATETIME的通用测试用例
def datetime_case():
    length = 19 #"2019-08-11 14:17:39"
    results = list()
    getstring = GetString()
    # 1 2019年正确日期时间
    results.append([f"2019年正确日期T", getstring.random_datetime(2019,2019)])
    # 2 错误月13月
    results.append([f"错误月13月","2018-13-11 14:17:39"])
    # 3 错误日12月32日
    results.append([f"错误日12月32日","2018-12-32 14:17:39"])
    # 4 错误时25时
    results.append([f"错误时25时","2019-05-11 25:10:59"])
    # 5 错误分60分
    results.append([f"错误分60分","2019-09-11 03:60:39"])
    # 6 错误秒60秒
    results.append([f"错误秒60秒","2018-11-11 11:11:60"])
    # 7 不存在的2月29日
    results.append([f"不存在的2月29日","2019-02-29 01:18:40"])
    # 8 秒有小数
    results.append([f"秒有小数","2017-12-11 14:17:39.12"])
    # 9 正确日期时间前后有空格
    results.append([f"正确日期时间前后有空格","  2019-01-11 22:17:37      "])
    # 10 正确日期与时间之间多个空格
    results.append([f"正确日期与时间之间多个空格","2019-03-11    08:22:09"])
    # 11 正确日期与时间之间没有空格
    results.append([f"正确日期与时间之间没有空格","2019-03-1108:22:09"])
    # 12 年份前多一个0
    results.append([f"年份前多一个0","02019-09-11 10:18:39"])
    # 13 日期为length位小写字母
    results.append([f"日期为{length}位的小写字母F", getstring.random_string_multiple(['ZMX'], length)])
    # 14 日期为length位的大写字母
    results.append([f"日期为{length}位的大写字母F", getstring.random_string_multiple(['ZMD'], length)])
    # 15 日期为length位的小写字母、数字
    results.append([f"日期为{length}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length)])
    # 16 日期为length位大写字母、数字
    results.append([f"日期为{length}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length)])
    # 17 日期为length位全角数字
    results.append([f"日期为{length}位全角数字F", getstring.random_string_multiple(['QJSZ'], length)])
    # 18 日期为length位的汉字
    results.append([f"日期为{length}位的汉字F", getstring.random_string_multiple(['HZ'], length)])
    # 19 日期为length位的繁体字
    results.append([f"日期为{length}位的繁体字F", getstring.random_string_multiple(['FT'], length)])
    # 20 日期为length位的难体字
    results.append([f"日期为{length}位的难体字F", getstring.random_string_multiple(['NT'], length)])
    # 21 日期为length位的特殊符号
    results.append([f"日期为{length}位的特殊符号F", getstring.random_string_multiple(['FH'], length)])
    # 22 日期为空值
    results.append(["日期为空值F", ''])
    # 23 日期为null值
    results.append(["日期为null值F", 'null'])
    # 24 sql注入 "or"1"="1
    results.append(["sql注入F", getstring.random_datetime(2019,2019)+ "''or''1''=''1"])
    logger.debug(results)
    return results


# 生成CHAR的通用测试用例
def int_case(length):
    length = int(length)
    results = list()
    getstring = GetString()
    # 1生成length位的正数
    results.append([f"生成{length}位的正数T", int(getstring.random_int_and_double(length))])
    # 2生成length+1位的正数
    results.append([f"生成{length+1}位的正数F", int(getstring.random_int_and_double(length+1))])
    # 3生成length位的正数（两边有空格）
    results.append([f"生成{length}位的正数（两边有空格）F", "   " + str(int(getstring.random_int_and_double(length))) + "  "])
    # 4生成length位的负数
    results.append([f"生成{length}位的负数F", int(getstring.random_int_and_double(length)) * -1])
    # 5生成length+1位的负数
    results.append([f"生成{length+1}位的负数F", int(getstring.random_int_and_double(length+1)) * -1])
    # 6生成length位的小写字母
    results.append([f"生成{length}位的小写字母F", getstring.random_string_multiple(['ZMX'], length)])
    # 7生成length位的大写字母
    results.append([f"生成{length}位的大写字母F", getstring.random_string_multiple(['ZMD'], length)])
    # 8生成length位的小写字母、数字
    if length >= 2:
        results.append([f"生成{length}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length)])
    # 9生成length位大写字母、数字
    if length >= 2:
        results.append([f"生成{length}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length)])
    # 10生成length位全角数字
    results.append([f"生成{length}位全角数字F", getstring.random_string_multiple(['QJSZ'], length)])
    # 11生成length位的汉字
    results.append([f"生成{length}位的汉字F", getstring.random_string_multiple(['HZ'], length)])
    # 12生成length位的繁体字
    results.append([f"生成{length}位的繁体字F", getstring.random_string_multiple(['FT'], length)])
    # 13生成length位的难体字
    results.append([f"生成{length}位的难体字F", getstring.random_string_multiple(['NT'], length)])
    # 14生成length位的特殊符号
    results.append([f"生成{length}位的特殊符号F", getstring.random_string_multiple(['FH'], length)])
    # 15生成空值
    results.append(["生成空值F", ''])
    # 16生成null值
    results.append(["生成null值F", 'null'])
    # 17sql注入 "or"1"="1
    results.append(["sql注入F", str(getstring.random_int_and_double(1)) + "''or''1''=''1"])
    return results


# 生成DOUBLE的通用测试用例
def double_case(length):
    length = int(length)
    results = list()
    getstring = GetString()
    ndigit = 8
    # 1生成length ndigit位的正小数
    results.append([f"生成{length},{ndigit}位的正小数T", getstring.random_int_and_double(length-ndigit,ndigit)])
    # 2生成length+1位的正小数
    # results.append([f"生成{length+1}位的正数F", getstring.random_int_and_double(length+1,ndigit)])
    # 3生成length位的正小数（两边有空格）
    results.append([f"生成{length},{ndigit}位的正小数（两边有空格）F", "   " + str(getstring.random_int_and_double(length-ndigit,ndigit)) + "  "])
    # 4生成length位的负小数
    results.append([f"生成{length},{ndigit}位的负小数F", getstring.random_int_and_double(length-ndigit,ndigit) * -1])
    # 5生成length+1位的负小数
    # results.append([f"生成{length+1}位的负数F", getstring.random_int_and_double(length+1,ndigit) * -1])
    # 6生成length位的小写字母
    results.append([f"生成{length}位的小写字母F", getstring.random_string_multiple(['ZMX'], length)])
    # 7生成length位的大写字母
    results.append([f"生成{length}位的大写字母F", getstring.random_string_multiple(['ZMD'], length)])
    # 8生成length位的小写字母、数字
    if length >= 2:
        results.append([f"生成{length}位的小写字母、数字F", getstring.random_string_multiple(['ZMX', 'SZ'], length)])
    # 9生成length位大写字母、数字
    if length >= 2:
        results.append([f"生成{length}位大写字母、数字F", getstring.random_string_multiple(['ZMD', 'SZ'], length)])
    # 10生成length位全角数字
    results.append([f"生成{length}位全角数字F", getstring.random_string_multiple(['QJSZ'], length)])
    # 11生成length位的汉字
    results.append([f"生成{length}位的汉字F", getstring.random_string_multiple(['HZ'], length)])
    # 12生成length位的繁体字
    results.append([f"生成{length}位的繁体字F", getstring.random_string_multiple(['FT'], length)])
    # 13生成length位的难体字
    results.append([f"生成{length}位的难体字F", getstring.random_string_multiple(['NT'], length)])
    # 14生成length位的特殊符号
    results.append([f"生成{length}位的特殊符号F", getstring.random_string_multiple(['FH'], length)])
    # 15生成空值
    results.append(["生成空值F", ''])
    # 16生成null值
    results.append(["生成null值F", 'null'])
    # 17sql注入 "or"1"="1
    results.append(["sql注入F", str(getstring.random_int_and_double(1,3)) + "''or''1''=''1"])
    return results


# temp_single 为内层报文
def generate_single_case_main(temp_single):
    excel_datas,common_datas = read_xls_single()
    logger.info(excel_datas)
    step = int(common_datas["step"])
    opsql = OperateMysql()
    for d in excel_datas:
        # [{'resquest_param': 'fp_dm','param_sort': 'VARCHAR', 'length': '10'},
        #  {'resquest_param': 'kprq', 'param_sort': 'DATETIME', 'length': ''}]
        temp = copy.deepcopy(temp_single)
        # temp = temp_single.copy() # 这个语法是浅拷贝，temp内层字典的值仍与temp_single是同一地址
        # 修改模板中发票代码
        temp['FPXX']['FP_KJ']['FPDM'] = "24" + time.strftime("%y%m") + "000240"

        if d["param_sort"].strip() == "VARCHAR":
            attr_datas = varchar_case(d["length"])
            # [['生成11位的数字', '34140688517'], ['生成12位的数字', '031856900374']]
        elif d["param_sort"].strip() == "CHAR":
            attr_datas = char_case(d["length"])
        elif d["param_sort"].strip() == "DATETIME":
            attr_datas = datetime_case()
        elif d["param_sort"].strip() == "INT":
            attr_datas = int_case(d["length"])
        elif d["param_sort"].strip() == "DOUBLE":
            attr_datas = double_case(d["length"])
        else:
            logger.error("输入的param_sort有误{}".format(d["param_sort"]))
            continue
        for l in attr_datas:
            step += 1
            # 修改模板中发票号码
            temp['FPXX']['FP_KJ']['FPHM'] = int(common_datas["fphm"]) + step
            common_datas["step"] = step
            common_datas["request_name"] = str(d["resquest_param"]) + "--" + l[0]
            common_datas["request_sql_param"] = generate_inner_param(temp,d["resquest_param"],l[1])
            opsql.insert_sql(common_datas)
        step += 40
    opsql.close()


# 将内层报文参数inner_param的值修改为inner_param_value并返回
def generate_inner_param(temp,inner_param,inner_param_value):
    inner_param = inner_param.upper()
    # 发票主信息
    if inner_param in temp['FPXX']['FP_KJ'].keys():
        temp['FPXX']['FP_KJ'][inner_param] = inner_param_value
    # 发票开具明细
    elif inner_param in temp['FPXX']['FP_KJ_MX'][0].keys():
        temp['FPXX']['FP_KJ_MX'][0][inner_param] = inner_param_value
    # 发票物流信息
    elif inner_param in temp['FPXX']['FP_WLXX'][0].keys():
        temp['FPXX']['FP_WLXX'][0][inner_param] = inner_param_value
    # 发票支付信息
    elif inner_param in temp['FPXX']['FP_ZFXX'].keys():
        temp['FPXX']['FP_WLXX'][0][inner_param] = inner_param_value
    else:
        logger.error(f"未找到{inner_param}!!!!!!!")

    return json.dumps(temp,ensure_ascii=False)


if __name__ == "__main__":
    generate_single_case_main(TEMPLATE_SINGLE)
    logger.warning("------end------！")

