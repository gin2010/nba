# -*- coding: utf-8 -*-
# @Date : 2019/8/26
# @Author : water
# @Desc  :根据excel表中的用例生成xml测试脚本
# @Version  :1.4
# @Modify : 1.4增加生成多条项目明细记录
#           1.3增加区分发票头信息()与发票项目明细信息()
#              将excel里的分隔符改成换行符



import os
import xlrd
import logging
#查看变量的装修器
import pysnooper as ps

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
AUTOCASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.dirname(AUTOCASE_PATH)
CASEDATA_PATH = os.path.join(DATA_PATH,"CaseData")
CHECKDATA_PATH = os.path.join(DATA_PATH,"CheckData")
TESTCASE_PATH = os.path.join(DATA_PATH,"TestCase")
POOL_PATH = os.path.dirname(DATA_PATH)


def insertDataIntoFile(filepath,data,findStr):
    '''

    :param filepath:要插入的文件
    :param data:插入的内容
    :param findStr:在哪个str前面插入（位置）
    :return:
    '''

    f = open(filepath,'r')
    content = f.read()
    f.close()
    num = content.find(findStr)
    content_new = content[:num] + data +"\n" + content[num:]
    f= open(filepath,'w')
    f.write(content_new)
    f.close()
#@ps.snoop()
def generateXml(values,nodes,outer=""):
    if outer == "":
        xml = ""
        for node,value in zip(nodes,values):
            xml += ("<{0}>{1}</{0}>\n").format(node,value)
        return xml
    else:
        xml = "<{}>\n".format(outer)
        for node,value in zip(nodes,values):
            xml += ("<{0}>{1}</{0}>\n").format(node,value)
        return xml + "</{}>\n".format(outer)

#@ps.snoop()
def generate_case(bh,vvalue_head,tvariable_head,vvalue_mx_list,tvariable_mx_list,file_name):
    '''
    生成caseData
    :param bh: 用例名与编号（默认相同）
    :param vvalue: 用例的变量值
    :param tvariable: 测试的某个变量（需要使用此变量建case的文件夹及xml里的节点）
    :return:
    '''
    case_file_name = bh + ".xml"
    case_file = os.path.join(CASEDATA_PATH,'SJPT','FPQZ',file_name,case_file_name)
    case_data = '''<?xml version="1.0" encoding="gb2312"?>
    <SJPT>
        <BH>{0}</BH>
        <ISCA />
        <ISDOWNLOAD />
        <REQUEST_FPQZ class="REQUEST_FPQZ">
        <FPQZ_INFO></FPQZ_INFO>
        <FPQZ_FPT class="FPQZ_FPT">
            {1}    
        </FPQZ_FPT>
        <FPQZ_XMXXS class="FPQZ_XMXX;" size="2">
            {2}
        </FPQZ_XMXXS>
        </REQUEST_FPQZ>
    </SJPT>
    '''
    if vvalue_head != "":
        tvariable_list_1 = tvariable_head.strip('\n').split(sep="\n")
        vvalue_list_1 = vvalue_head.strip('\n').split(sep="\n")
    else:
        vvalue_list_1=tvariable_list_1=""
    case_head_xml = generateXml(vvalue_list_1,tvariable_list_1)
    #生成多条发票明细
    case_mx_xml = ""
    for i in range(len(vvalue_mx_list)):
        if vvalue_mx_list[i] != "":
            tvariable_list_2 = tvariable_mx_list[i].strip('\n').split(sep="\n")
            vvalue_list_2 = vvalue_mx_list[i].strip('\n').split(sep="\n")
            mx_xml = generateXml(vvalue_list_2, tvariable_list_2, "FPQZ_XMXX")
        case_mx_xml += mx_xml
    with open(case_file,'w') as f:
        f.writelines(case_data.format(bh,case_head_xml,case_mx_xml))
        logger.warning('casedata generate success')


def generate_check(bh):
    '''
    生成checkData
    :param bh: 用例名与编号（默认相同）
    :return:
    '''
    check_data = """
    <CheckPoint>
        <Bh>{}</Bh>
        <RetMsg>
          <Code>0000</Code>
          <Msg>接收发票开具数据成功！</Msg>
        </RetMsg>	
    </CheckPoint>""".format(bh)
    findStr =  "</CasePool>"
    filepath = os.path.join(CHECKDATA_PATH,"开具_check_DZ电子.xml")
    insertDataIntoFile(filepath,check_data,findStr)
    logger.warning('checkdata generate success')

# @ps.snoop()
def generate_test(bh):
    '''
    生成testData
    :param bh: 用例名与编号（默认相同）
    :return:
    '''
    test_data = """
    <TestCase>
        <Bh>{0}</Bh>
        <CaseName>{0}</CaseName>
        <CaseId>UCSEC1</CaseId>
        <Description>发票签章成功，对比数据库</Description>
        <Step id="1">
            <Name>发票签章</Name>
            <Keyword>FPQZ</Keyword>
            <SubKeyword>Template</SubKeyword>
            <param name="DATABHS">{0}</param>
            <param name="ISSYNC">false</param>
            <param name="INTERFACECODE">ECXML.FPQZ.BC.E.INV</param>
        </Step>
        <Step id="2">
            <Name>数据比对</Name>
            <Keyword>CHECK</Keyword>
            <param name="DATABHS">{0}</param>
        </Step>
    </TestCase> 
    """.format(bh)
    findStr = "</CasePool>"
    filepath = os.path.join(TESTCASE_PATH,"case.xml")
    insertDataIntoFile(filepath,test_data,findStr)
    logger.warning('testdata generate success')


def add_pool(bh):
    '''
    向testcasepool中增加用例编号
    :param bh:用例名与编号（默认相同）
    :return:
    '''
    pool_data = """
    <Bh>{}</Bh> 
    """.format(bh)
    findStr = "</CasePool>"
    filepath = os.path.join(POOL_PATH,"TestCasePool.xml")
    insertDataIntoFile(filepath,pool_data,findStr)
    logger.warning('pool add success')


def auto_main(bh,vvalue_head,tvariable_head,vvalue_mx,tvariable_mx,filename):
    generate_case(bh, vvalue_head,tvariable_head,vvalue_mx,tvariable_mx,filename)
    generate_check(bh)
    generate_test(bh)
    add_pool(bh)


# 读excel中的用例，add by water,20190822
# @ps.snoop()
def read_excel(filename):
    excel_path = os.path.join(AUTOCASE_PATH, 'case', filename + ".xls")
    sheet1 = xlrd.open_workbook(excel_path).sheet_by_index(0)
    max_row = sheet1.nrows
    max_column = sheet1.ncols
    case_names = sheet1.col_values(1, 0, max_row)
    tvariables_head = sheet1.col_values(2, 0, max_row)
    variable_values_head = sheet1.col_values(3, 0, max_row)
    tvariables_mx  = list()
    variable_values_mx = list()
    for r in range(0,max_row):
        tvariable_mx = list()
        variable_value_mx = list()
        for c in range(4,max_column,2):
            mx_code = sheet1.cell(r,c).value
            mx_value = sheet1.cell(r,c+1).value
            if len(mx_code)>0 and len(mx_value)>0:
                tvariable_mx.append(mx_code)
                variable_value_mx.append(mx_value)
                # print("variable_value_mx:",variable_value_mx)
        tvariables_mx.append(tvariable_mx)
        variable_values_mx.append(variable_value_mx)
    return (case_names,variable_values_head,tvariables_head,variable_values_mx,tvariables_mx,max_row)


#判断是否需要在Data\CaseData\SJPT\FPQZ下新建用例文件夹
def exist_case_dir(tvariable):
    case_dir = os.path.join(CASEDATA_PATH, 'SJPT', 'FPQZ', tvariable)
    if not os.path.exists(case_dir):
        os.makedirs(case_dir)
    logger.info(f'---case in {case_dir}---')


if __name__ == "__main__":

    logger.info("-----Start-----")
    filename = "FPQZ_GZ"
    exist_case_dir(filename)
    (case_names,variable_values_head,tvariables_head,variable_values_mx,tvariables_mx,max_row) = read_excel(filename)
    logger.info("max_row:{}".format(max_row))
    for i in range(max_row):
        auto_main(case_names[i],variable_values_head[i],tvariables_head[i],variable_values_mx[i],tvariables_mx[i],filename)
        logger.info(f"---{case_names[i]} success---")
    logger.info(f"---{filename} Finish----")

