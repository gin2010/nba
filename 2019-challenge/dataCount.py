# -*- coding: utf-8 -*-
# @Date : 2019/11/06
# @Author : water
# @Version  : v1.0
# @Desc  : 分类汇总excel表中的数据

import xlrd,openpyxl,os,logging
import pandas as pd

##配置文件
LOG_LEVEL = 0  # DEBUG(10)<INFO(20)<WARN(30)<ERROR(40)<CRITICAL(50)



class DataCount(object):

    def __init__(self):
        self.excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"测试评价部-测试开发部-测试周报.xls")
        logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s- %(levelname)s- %(message)s:')
        self.logger = logging.getLogger(__name__)

    def _read_excel_to_clean(self):
        '''
        -->先读取数据；
        -->合并sheet，并把sheet名作为日期列添加到每个表格中；
        -->填充na值
        -->拆分一个单元格中有多个值的情况（分隔符为"\n"）
        :return:
        '''
        wb = xlrd.open_workbook(self.excel_path)
        self.logger.debug(wb.sheet_names())
        sheets_list = wb.sheet_names()
        # 将测试人员列、工时列多值拆成不同的行中
        data = pd.read_excel(self.excel_path)
        # 用上一行的数据替换掉na值，除第一行
        data = data.fillna(method ="ffill")
        # 第一行为na的替换为空
        data = data.fillna("")
        self.logger.debug(data.head(10))
        # for sheet_index in range(len(sheets_list)):
        #     datas = pd.read_excel(self.excel_path, sheet_name=sheet_index)
        #     datas["日期"] = sheets_list[sheets_list]
        #     self.logger.debug(a.split(sep="\n"))

    def _to_excel(self):
        pass


    def _query_data(self):
        pass


if __name__ =="__main__":
    result = DataCount()
    result._read_excel_to_clean()