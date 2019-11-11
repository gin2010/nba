# -*- coding: utf-8 -*-
# @Date : 2019/11/06
# @Author : water
# @Version  : v1.0
# @Desc  : 分类汇总excel表中的数据

import xlrd,openpyxl,os,logging
import pandas as pd
import re

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
        data = pd.read_excel(self.excel_path,dtype=str)
        # 用上一行的数据替换掉na值，除第一行
        data = data.fillna(method ="ffill")
        # 第一行为na的替换为空
        data = data.fillna("")
        # 去掉标题中的回车符与空格

        # 去掉数据中空格
        data = self._seperate_multiple_datas(data,["测试人员","工时（人日）"])
        data1 = data["测试人员"].str.split("\n",expand=True)
        self.logger.debug(data1)
        data = data.reindex(columns=["测试产品线","研发负责人","测试人员","工时（人日）"])
        self.logger.debug(print(data.head(19)))
        # for sheet_index in range(len(sheets_list)):
        #     datas = pd.read_excel(self.excel_path, sheet_name=sheet_index)
        #     datas["日期"] = sheets_list[sheets_list]
        #     self.logger.debug(a.split(sep="\n"))



    def _seperate_multiple_datas(self,data,columns):
        '''
        将同一单元格有多个换行的数据拆分成独立的行，拆分前先验证拆分的单元格都是同样长度
        :param data: 数据表
        :param columns: 需要拆分的列
        :return:
        '''
        max_row,max_column = data.shape
        length = len(columns)
        # 去掉数据列中的空格
        for column in columns:
            data[column] = data[column].apply(str.strip)
            data[column] = data[column].apply(lambda x: re.sub(r"\s{2,}", "\n", x))

        first = data.loc[:1]
        target = data2[1:2]
        last = data2[2:]
        values = target.at[1, "name"].split(",")
        new1 = pd.DataFrame(values[1:], columns=["name"])
        pd.concat([first, target, new1, last], ignore_index=True, sort=False)




        return data


    def _to_excel(self):
        pass


    def _query_data(self):
        pass


if __name__ =="__main__":
    result = DataCount()
    result._read_excel_to_clean()