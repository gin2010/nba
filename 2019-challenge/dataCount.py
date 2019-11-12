# -*- coding: utf-8 -*-
# @Date : 2019/11/06
# @Author : water
# @Version  : v1.0
# @Desc  : 分类汇总excel表中的数据

import xlrd,xlwt,os,logging
import pandas as pd
import re
from xlutils.copy import copy

##配置文件
LOG_LEVEL = 0  # DEBUG(10)<INFO(20)<WARN(30)<ERROR(40)<CRITICAL(50)



class DataCount(object):

    def __init__(self):
        self.department = "系统测试部"
        self.excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"测试评价部-系统测试部-测试周报.xlsx")
        logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s- %(levelname)s- %(message)s:')
        self.logger = logging.getLogger(__name__)
        # 配置获取最大列数
        self.max_column = 16
        # fomatting_info 参数不支持xlsx
        # self.wb = xlrd.open_workbook(self.excel_path, formatting_info=True)
        self.wb = xlrd.open_workbook(self.excel_path)
        self.sheets_list = self.wb.sheet_names()
        self.new_wb = xlwt.Workbook(encoding='utf-8')


    # 填充合并单元格、拆分多值单元格为多行
    def _fill_merge_cell_and_split(self,sheet_name):
        sheet = self.new_wb.add_sheet(sheet_name,cell_overwrite_ok=True)
        ws = self.wb.sheet_by_name(sheet_name)
        self.logger.debug(sheet_name)
        # 获得合并单元格区域的列表
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
        # 合并单元格的空值使用第一个值填充
        target_r = 0   # 目标sheet写入的行数
        for r in range(0,ws.nrows):
            # 去掉空行
            if len([x.value for x in ws.row(r) if x.value != ""]) == 0:
                continue
            # 判断本行的测试人员是不是多个，如果是就将人员（name)、工时(workhour)拆成列表再写入sheet中
            if len(self._del_blank_and_return(ws.cell(r,10).value)) > 1:
                name = self._del_blank_and_return(ws.cell(r,10).value)
                self.logger.debug(name)
                workhour = self._del_blank_and_return(ws.cell(r,11).value)
                self.logger.debug(workhour)
                for i in range(len(self._del_blank_and_return(ws.cell(r,10).value))):
                    for c in range(self.max_column + 1):
                        row_value, column_value = self._get_cell_value((r, c), merge_sections)
                        sheet.write(target_r, c, ws.cell(row_value, column_value).value)
                    sheet.write(target_r, 10, name[i])
                    try:
                        sheet.write(target_r, 11, workhour[i])
                    except IndexError:
                        self.logger.error("sheet:{} 单元格({},{})填写有误，已将空值置为0！".format(sheet_name,r+1,12))
                        sheet.write(target_r, 11, 0)
                    target_r += 1
                    # 将sheet_name值添加为新列“期间”
                    sheet.write(target_r, self.max_column + 1, sheet_name)
                    sheet.write(target_r, self.max_column + 2, self.department)
            else:
                for c in range(self.max_column + 1):
                    row_value, column_value = self._get_cell_value((r, c), merge_sections)
                    sheet.write(target_r, c, ws.cell(row_value, column_value).value)
                target_r += 1
            #将sheet_name值添加为新列“期间”
            sheet.write(target_r,self.max_column+1,sheet_name)
            sheet.write(target_r, self.max_column + 2, self.department)
        sheet.write(0,self.max_column + 1,"期间")
        sheet.write(0, self.max_column + 2, "二级部门")
        # 加一个对列标题的处理


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
        value = replace_blank(str(value))
        if value == "":
            return []
        else:
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


    def _load_data(self):
        '''
        -->加载数据；
        -->合并sheet
        -->统计报表
        -->写入到excel表中
        :return:
        '''
        wb = xlrd.open_workbook(self.excel_path)
        #data = pd.DataFrame(data=list(zip(ws.col_values(1), ws.col_values(2))), columns=["aa", "bb"])
        self.logger.debug(wb.sheet_names())
        sheets_list = wb.sheet_names()
        # 将测试人员列、工时列多值拆成不同的行中
        data = pd.read_excel(self.excel_path,dtype=str)
        # 用上一行的数据替换掉na值，除第一行
        # data = data.fillna(method ="ffill")
        # 第一行为na的替换为空
        data = data.fillna("")
        # 去掉标题中的回车符与空格

        # 去掉数据中空格
        data = self._seperate_multiple_datas(data,["测试人员","工时（人日）"])
        data1 = data["测试人员"].str.split("\n",expand=True)
        self.logger.debug(data1)
        data = data.reindex(columns=["测试产品线","工作项目/任务","研发\n负责人"])
        self.logger.debug(print(data.head(22)))
        # for sheet_index in range(len(sheets_list)):
        #     datas = pd.read_excel(self.excel_path, sheet_name=sheet_index)
        #     datas["日期"] = sheets_list[sheets_list]
        #     self.logger.debug(a.split(sep="\n"))




    def _to_excel(self):
        pass


    def _query_data(self):
        pass

    def main(self):
        for sheet_name in self.sheets_list:
            self._fill_merge_cell_and_split(sheet_name)
        self.new_wb.save("./temp/666.xls")
        self.logger.warning("报表数据清洗成功！！！")

if __name__ =="__main__":
    result = DataCount()
    result.main()

