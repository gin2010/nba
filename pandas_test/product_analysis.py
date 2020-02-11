# -*- coding: utf-8 -*-
# @Date : 2020-01-17
# @Author : water
# @Version  : v1.0
# @Desc  :

import pandas as pd
import numpy as np
import os,xlrd,configparser

PATH = os.path.dirname(os.path.abspath(__file__))
file_name = "资管中心2019年四季度新产品绩效评价.xlsx"  # 写入配置
file_path = os.path.join(PATH,'datas',file_name)
target_column = "最近三月总回报(%)"
annual_income = "年化收益率"
rank_column = "排名"

def main():
    datas = pd.read_excel(file_path,sheet_name="万得",header=None) # sheetname写入配置
    print(datas.head())
    column_names = list(datas.loc[0].fillna('') + datas.loc[1])
    datas.columns=column_names # 重置列名
    datas = datas.iloc[2:] # 删除前两行的数据，数据清洗完成
    print("列标题为：",datas.columns)
    # 数据排序 rank(method='min')
    datas[annual_income] = datas['最近三月总回报(%)'] * 4 / 100
    datas[annual_income] = datas[annual_income].fillna(0)
    datas[rank_column] = datas[annual_income].groupby(datas['投资类型']).rank(method='min',ascending=False)
    datas.to_excel("123.xls")


if __name__ == "__main__":
    main()

