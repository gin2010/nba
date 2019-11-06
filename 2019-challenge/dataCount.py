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
        wb = xlrd.open_workbook(self.excel_path)
        #self.logger.debug(wb.sheet_names())
        #sheets_list = wb.sheet_names()
        datas = pd.read_excel(self.excel_path)
        a = datas.at[3,"测试人员"]
        self.logger.debug(a.split(sep="\n"))
        #将测试人员列、工时列多值拆成不同的行中


    def _to_excel(self):
        pass


    def _query_data(self):
        pass


if __name__ =="__main__":
    result = DataCount()
    result._read_excel_to_clean()