# coding:utf-8
# author:water
import pandas as pd
import os
import pysnooper as ps


DIR = "experience"

@ps.snoop(prefix="****")
def file(DIR):
    filepath = os.path.join(os.getcwd(),DIR)
    excel_files= []
    for root,dir1,files in os.walk(filepath):
        for file in files:
            excel_files.append(os.path.join(filepath,file))
    return excel_files



if __name__ == "__main__":
    data = []
    result = os.path.join(os.getcwd(),DIR,DIR+".xlsx")
    excel_files = file(DIR)
    for excel_file in excel_files:
        data.append(pd.read_excel(excel_file))

    pd.concat(data).to_excel(result,DIR,index=False)





