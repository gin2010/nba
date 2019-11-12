# -*- coding: utf-8 -*-
# @Date : 2019/11/06
# @Author : water
# @Version  : v1.0
# @Desc  : 这里面有填充合并单元格_fill_merge_cell与拆分多值单元格_split_cell单独的方法

import xlrd,xlwt,os,logging
import pandas as pd
import re
from xlutils.copy import copy

##配置文件
LOG_LEVEL = 0  # DEBUG(10)<INFO(20)<WARN(30)<ERROR(40)<CRITICAL(50)



class DataCount(object):

    def __init__(self):
        self.excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"测试评价部-测试开发部-测试周报.xls")
        logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s- %(levelname)s- %(message)s:')
        self.logger = logging.getLogger(__name__)
        # 配置获取最大列数
        self.max_column = 16
        self.wb = xlrd.open_workbook(self.excel_path, formatting_info=True)
        self.sheets_list = self.wb.sheet_names()
        self.new_wb = xlwt.Workbook(encoding='utf-8')


    # 填充合并单元格
    def _fill_merge_cell(self,sheet_name):
        '''
        读取excel时候会将合并单元格拆开并将值只填入到第一个单元格中，
        此函数功能将所有的合并单元格的值补充
        :param sheet_name:excel sheet的名字
        :return:
        '''
        sheet = self.new_wb.add_sheet(sheet_name,cell_overwrite_ok=True)
        ws = self.wb.sheet_by_index(0)
        merge_cell = ws.merged_cells
        self.logger.debug(merge_cell)
        merge_sections = list()
        for section in merge_cell:
            first_row,last_row,col,_ = section
            merge_section = list()
            for row in range(first_row,last_row):
                merge_section.append((row,col))
            merge_sections.append(merge_section)
        self.logger.debug("合并单元格的区域：" + str(merge_sections))

        for r in range(ws.nrows):
            for c in range(self.max_column+1):
                row_value,column_value = self._get_cell_value((r,c),merge_sections)
                sheet.write(r, c, ws.cell(row_value, column_value).value)
            sheet.write(r,self.max_column+1,sheet_name)
        sheet.write(0,self.max_column+1,"期间")
        # 加一个对列标题的处理


    # 拆分多值单元格
    def _split_cell(self, sheet_name):
        '''
        针对一个单元格中通过回车符、空格之类填入多个值，将此单元格拆分为多行，
        其他列的值保持不变
        此程序中第10列是测试人员，第11列是对应的工时
        :param sheet_name: excel sheet的名字
        :return:
        '''
        new_wb = xlwt.Workbook(encoding='utf-8')
        sheet = new_wb.add_sheet(sheet_name, cell_overwrite_ok=True)
        wb2 = xlrd.open_workbook("./temp/444.xls")
        ws2 = wb2.sheet_by_index(0)
        self.logger.debug(ws2.col_values(10))
        self.logger.debug(ws2.col_values(11))
        target_r = 0
        for r in range(0, ws2.nrows):
            if len(self._del_blank_and_return(ws2.cell(r, 10).value)) > 1:
                name = self._del_blank_and_return(ws2.cell(r, 10).value)
                self.logger.debug(name)
                workhour = self._del_blank_and_return(ws2.cell(r, 11).value)
                self.logger.debug(workhour)
                for i in range(len(self._del_blank_and_return(ws2.cell(r, 10).value))):
                    for c in range(self.max_column + 1):
                        sheet.write(target_r, c, ws2.cell(r, c).value)
                    sheet.write(target_r, 10, name[i])
                    sheet.write(target_r, 11, workhour[i])
                    target_r += 1
            else:
                for c in range(self.max_column + 1):
                    sheet.write(target_r, c, ws.cell(r, c).value)
                target_r += 1
                sheet.write(target_r, c, ws2.cell(r, c).value)
        new_wb.save("./temp/aaa.xls")


    def _get_cell_value(self,section,merge_sections):
        '''
        判断是否是合并单元格：
        如果是合并单元格，则返回合并单元格第一个单元格所在的位置；
        如果不是合并单元格，则返回的还是section
        :param self:
        :param section: 当前单元格位置（row,column）
        :param merge_sections: 全部合并单元格区域
            [[(0,1),(1,1)],[(1,3),(2,3),(3,3)],[...]]
            其中列表中第一个值为合并单元格取消合并后值所在的位置
        :return: 当前单元格实际值所在的位置
        '''
        for i in range(len(merge_sections)):
            if section in merge_sections[i]:
                return merge_sections[i][0]
        else:
            return section


    def _del_blank_and_return(self,value):
        '''
        处理多值单元格：对多值单元格格式化，去掉两边的空格、回车符，并将中间的空格替换为"\n"
        :param self:
        :param value:某个单元格的值
        :return:格式化后的值
        '''
        replace_blank = lambda x: re.sub(r"\s{2,}", "\n", x)
        value = replace_blank(value)
        return value.strip().split("\n")



    def _merge_sheet(self):

        datas = pd.DataFrame()
        for sheet in self.sheets_list:
            print(sheet)
            # skiprows=0代表读取跳过的行数为0行，不写代表不跳过标题
            data = pd.read_excel(self.excel_path, sheet_name=sheet, skiprows=1, index=False, encoding='utf8')
            datas = datas.append(data)
            print("---datas----\n",datas)
        datas.to_excel("./333.xls",sheet_name="datas")






    def main(self):
        for sheet_name in self.sheets_list:
            self._fill_merge_cell(sheet_name)
        self.new_wb.save("./temp/555.xls")


if __name__ =="__main__":
    result = DataCount()
    result.main()

