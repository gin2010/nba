# -*- coding: utf-8 -*-
# @Date : 2019/11/06
# @Author : water
# @Version  : v1.0
# @Desc  : 分类汇总excel表中的数据

import xlrd,xlwt,os,logging
import pandas as pd
import numpy as np
import re,time
from xlutils.copy import copy

##配置文件
LOG_LEVEL = 30  # DEBUG(10)<INFO(20)<WARN(30)<ERROR(40)<CRITICAL(50)
TITLES = ['序号', '测试产品线', '工作项目/任务', '任务来源', '任务性质', '测试负责人', '研发负责人', '本周工作目标',
          '实际完成时间', '实际完成情况', '测试人员', '工时', '事业部', '亮点', '问题点', '修改内容简述', '备注']
DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class DataCount(object):

    def __init__(self):
        self.weekly_xt = "测试评价部-系统测试部-测试周报.xlsx"
        self.weekly_ck = "测试评价部-测试开发部-测试周报.xls"
        self.temp_xt = os.path.join(DIR_PATH,"temp","data_xt.xls")
        self.temp_ck = os.path.join(DIR_PATH,"temp","data_ck.xls")
        self.total = os.path.join(DIR_PATH,"temp","total.xls")
        logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s- %(levelname)s- %(message)s:')
        self.logger = logging.getLogger(__name__)
        # 配置获取周报最大列数(由于从0开始，所以实际是17列)
        self.max_column = 16


    def _open_excel(self,excel_name):
        excel_path = os.path.join(DIR_PATH, excel_name)
        if excel_name.endswith("xls"):
            # fomatting_info 参数不支持xlsx，但xls格式如果不加此参数则无法获得合并区域
            wb = xlrd.open_workbook(excel_path,formatting_info=True)
        else:
            wb = xlrd.open_workbook(excel_path)
        sheets_list = wb.sheet_names()
        department = excel_name[(excel_name.find("-")+1):(excel_name.find("-",excel_name.find("-")+1))]
        self.logger.debug("department:{}".format(department))
        return wb,department


    # 填充合并单元格、拆分多值单元格为多行，一次处理的是一个sheet
    def _fill_merge_cell_and_split(self,wb,sheet_name,wb_new,department):
        # 新建写入excel的sheet
        sheet = wb_new.add_sheet(sheet_name,cell_overwrite_ok=True)
        # 打开周报对应sheet
        ws = wb.sheet_by_name(sheet_name)
        self.logger.debug("正在处理sheet:{}....".format(sheet_name))
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
                workhour = self._del_blank_and_return(ws.cell(r,11).value,False)
                self.logger.debug(workhour)
                for i in range(len(self._del_blank_and_return(ws.cell(r,10).value))):
                    for c in range(self.max_column + 1):
                        row_value, column_value = self._get_cell_value((r, c), merge_sections)
                        sheet.write(target_r, c, ws.cell(row_value, column_value).value)
                    sheet.write(target_r, 10, self._del_blank_and_return(name[i]))
                    try:
                        sheet.write(target_r, 11, workhour[i])
                    except IndexError:
                        self.logger.error("sheet:{} 单元格({},{})填写有误，已将空值置为0！".format(sheet_name,r+1,12))
                        sheet.write(target_r, 11, 0)
                    target_r += 1
                    # 将sheet_name值添加为新列“期间”
                    # sheet.write(target_r-1, self.max_column + 1, sheet_name)
                    # sheet.write(target_r-1, self.max_column + 2, department)
            else:
                for c in range(self.max_column + 1):
                    row_value, column_value = self._get_cell_value((r, c), merge_sections)
                    if c==10:
                        sheet.write(target_r, c, self._del_blank_and_return(ws.cell(row_value, column_value).value))
                    else:
                        sheet.write(target_r, c, ws.cell(row_value, column_value).value)
                target_r += 1
            #将sheet_name值添加为新列“期间”
            # sheet.write(target_r-1,self.max_column+1,sheet_name)
            # sheet.write(target_r-1, self.max_column + 2, department)
        # 列标题统一
        sheet.write(0,self.max_column + 1,"期间")
        sheet.write(0, self.max_column + 2, "二级部门")
        for c in range(self.max_column + 1):
            sheet.write(0, c, TITLES[c])
        # 写入期间与二级部门
        for i in range(1,target_r):
            sheet.write(i,self.max_column+1,sheet_name)
            sheet.write(i, self.max_column + 2, department)



    def _clear_data(self):
        # 汇总并清洗系统测试周报
        wb_xt,department = self._open_excel(self.weekly_xt)
        # 新建xlwt表格来写入excel数据
        wb_new_xt = xlwt.Workbook(encoding='utf-8')
        for sheet_name in wb_xt.sheet_names():
            self._fill_merge_cell_and_split(wb_xt, sheet_name,wb_new_xt,department)
            wb_new_xt.save(self.temp_xt)
        self.logger.warning("系统测试周报数据清洗成功！！！")

        # 汇总并清洗测试开发周报
        wb_ck,department = self._open_excel(self.weekly_ck)
        # 新建xlwt表格来写入excel数据
        wb_new_ck = xlwt.Workbook(encoding='utf-8')
        for sheet_name in wb_ck.sheet_names():
            self._fill_merge_cell_and_split(wb_ck, sheet_name,wb_new_ck,department)
            wb_new_ck.save(self.temp_ck)
        self.logger.warning("测试开发周报数据清洗成功！！！")



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


    def _del_blank_and_return(self,value,is_str=True):
        '''
        处理多值单元格：对多值单元格格式化，去掉两边的空格、回车符，并将中间的空格替换为"\n"
        :param self:
        :param value:某个单元格的值
        :return:格式化后的值
        '''
        invalid_list= ["河北","总部","河北：",""]
        replace_blank = lambda x: re.sub(r"\s{2,}", "\n", x)
        del_bracket = lambda y: re.sub(r"[\\(\\（].*?[\\)\\）]", "", y)
        del_order = lambda z: re.sub(r'^\d\.','',z)
        value = replace_blank(str(value)) #将多个值之前的回车、空格转为一个回车
        value = del_bracket(value)  # 去掉值后面的括号
        if is_str:
            value = del_order(value)  # 去掉值最前面的1.或2.
        self.logger.debug(value)
        if value == "":
            return []
        else:
            value_list = value.strip().split("\n")
            self.logger.debug(value_list)
            for key in invalid_list:
                if key in value_list:
                    value_list.remove(key)
                if "李" in value_list and "娟" in value_list:
                    value_list.remove("李")
                    value_list.remove("娟")
                    value_list.append("李娟")
            return value_list



    def _merge_data(self,temps):
        '''
        将清洗后的数据合并到一张表，并加载到dataFrame中
        :param temps: 清洗后的数据存放的excel表名（list）
        :return: datas合并后的数据（DataFrame格式）
        '''

        datas = pd.DataFrame()
        for temp in temps:
            # 从清洗后的temp文件里获取sheet_name
            wb_data = xlrd.open_workbook(temp)
            sheets_list = wb_data.sheet_names()
            for sheet in sheets_list:
                print(sheet)
                # skiprows=0代表读取跳过的行数为0行，不写代表不跳过标题
                data = pd.read_excel(temp, sheet_name=sheet, skiprows=0, index=False,header=0,encoding='utf8')
                datas = datas.append(data)
                self.logger.debug("---datas----\n",datas)
            # datas.to_excel(self.total,sheet_name=temp[-11:-4])
            self.logger.warning("{}数据合并成功！！！".format(temp[-11:]))
        # 去掉序号为0的数据（系统测试部周报则忽略第2-5行举例数据）
        datas = datas[datas.序号 != 0]
        # 工时里的空值用0来填充
        datas["工时"] = datas["工时"].fillna(0)
        # 测试人员为nan时，工时置为0
        datas.loc[pd.isna(datas["测试人员"]) == True, "工时"] = 0
        self.logger.warning(datas)
        datas.to_excel(self.total, sheet_name="total")
        return datas

    # 对DataFrame中的数据进行查询、统计
    def _data_analysis(self,datas,start,end):
        data["期间"] = data["期间"].apply(str) #将期间列由int转为str
        data["期间"] = pd.to_datetime(data["期间"]) # 将str转为日期格式
        data["工时"] = data["工时"].apply(float) # 工时转为float
        data.set_index('期间', drop=True, inplace=True) #重置索引列，并将原索引列删除
        data["2019-08":"2019-10"] #查询
        pd.pivot_table(data1,index=["事业部"],columns=["事业部","工作项目/任务","测试人员"],values=["测试人员","工时"],aggfunc=[np.sum])
        data.drop(['序号', '任务来源', '任务性质', '测试负责人', '研发负责人', '本周工作目标',
                   '实际完成时间', '实际完成情况', '亮点', '问题点', '修改内容简述', '备注'])
        agg1 = {"工时":["sum"]}
        result = data1.groupby(["事业部", "工作项目/任务","测试人员"]).agg(agg1)
        result2 = data1.groupby(["事业部", "工作项目/任务"]).agg(agg1)
        result["total"] = result2["工时"]
        result.reset_index(level=[0, 1, 2], inplace=True)
        result.set_index(["事业部", "工作项目/任务","测试人员","total"], drop=True, inplace=True)
        pd.pivot_table(data1, index=["事业部", "测试产品线", "测试人员"], values=["工时"])
        pd.pivot_table(data1, index=["事业部", "测试产品线", "测试人员"], values=["工时"], aggfunc=np.sum)
        result.to_excel("./report.xls")


    def main(self):
        # 对周报中数据清洗、格式统一
        self._clear_data()
        # 合并两个部门的周报为一个excel
        datas = self._merge_data([self.temp_xt,self.temp_ck])
        # 查询数据出报表
        #self._data_analysis(datas)


if __name__ =="__main__":
    result = DataCount()
    result.main()

