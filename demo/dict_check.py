# -*- coding: utf-8 -*-
# @Date : 2019-12-04
# @Author : water
# @Version  : v1.0
# @Desc  :

import xlrd,json

wb = xlrd.open_workbook("case.xls")
ws = wb.sheet_by_index(0)
max_row = ws.nrows
for i in range(1,ws.nrows):
    d = dict()
    d = ws.cell(i,2).value
    # try:
    #     if isinstance(json.loads(d), dict):
    #         continue
    #     else:
    #         print("row:{} value:{}".format(i, d))
    # except Exception:
    #     print("row:{} value:{}".format(i, d))

    if isinstance(json.loads(d), dict):
        continue
    else:
        print("row:{} value:{}".format(i, d))


