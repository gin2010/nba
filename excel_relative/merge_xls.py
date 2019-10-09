# coding:utf-8
# author:water
import xlrd, openpyxl, os,math

'''
读取代码所在文件里 education/experience文件下的xls文件，
并将每个文件下的xls文件合并为一个，并以文件夹名字命名
**由于xlwt只能保存为xls格式，因此不能超过65536行
'''
FILE = "experience"
file_path = os.path.join(os.getcwd(), FILE)
RESULT = os.path.join(file_path, FILE + ".xlsx")
datas = []


def file_name(file_dir):
    list_files = list()
    for root, dirs, files in os.walk(file_dir):
        # print("root：",root) #当前目录路径
        # print("dirs:",dirs) #当前路径下所有子目录
        for file in files:  # 获取目录下全部xls文件
            list_files.append(os.path.join(file_dir, file))
    return list_files


# 读取xls中的内容，并返回datas，二维列表
def merge(file):
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name(wb._sheet_names[0])
    row = sheet.nrows
    # col = sheet.ncols
    for i in range(row):
        datas.append(sheet.row_values(i))


if __name__ == "__main__":
    files = file_name(file_path)
    for file in files:
        merge(file)
    print("******merge start*******")
    workbook = openpyxl.Workbook()
    sheet_num = 1
    worksheet = workbook.create_sheet(index=0)
    for i in range(len(datas)):
        for j in range(len(datas[i])):
            worksheet.cell(i+1, j+1, datas[i][j])
    workbook.save(RESULT)
    print("******merge finish*******")


