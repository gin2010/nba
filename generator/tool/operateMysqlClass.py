# -*- coding: utf-8 -*-
# File  : OperateMysqlClass.py
# Author: water
# Date  : 2019/9/11

import pymysql
import logging

#程序运行日志配置
logging.basicConfig(level = logging.WARN,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

class OperateMysql:
    def __init__(self,host="172.16.22.37",port=3306,user="root",password="Sa!@#$%^",database="51fppt_test"):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        #连接数据库
        self.db = pymysql.connect(
            host=self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.database
        )
        #使用cursor()方法创建一个游标对象
        self.cursor = self.db.cursor()
        logger.warning("connect mysql successful!!")


    #关闭游标和数据库的连接
    def close(self):
        self.cursor.close()
        self.db.close()
        logger.warning("mysql closed!!")


    def insert_sql(self,data):

        # 插入数据
        sql = '''INSERT INTO step_data (case_id, step,test_desc,http_method,url_sql,out_put,request_sql_param,request_name) VALUES ('{case_id}','{step}','{test_desc}','{http_method}','{url_sql}','{out_put}','{request_sql_param}','{request_name}')'''
        sql = sql.format(**data)
        logger.info(sql)
        self.cursor.execute(sql)
        self.db.commit()
        logger.warning(f"step:{data['step']}&&{data['request_name']}插入成功")


if __name__ =="__main__":
    opsql = OperateMysql()
    case_id = 24230001
    step = 9
    test_desc = "测试数据库2"
    http_method = "post"
    url_sql = ""
    out_put = ""
    request_sql_param = {
        "YFPDM": "1238",
        "JQBH": "661505060904",
        "KPY": "开票员",
        "SKY": "收款员",
        "FHR": "复核人",
        "SWJG_DM": "111019201",
        "SPHSL": "1",
        "FP_ZLDM": "2",
        "VERSION": "1",
        "XSF_DZ": "北京市海淀区春晖园2号楼",
        "XSF_DH": "123123123",
        "XSF_YH": "1236",
        "XSF_YHZH": "招商银行"}
    request_name = 0
    data = {
        "case_id": case_id,
        "step": step,
        "test_desc": test_desc,
        "http_method": http_method,
        "url_sql": url_sql,
        "request_sql_param": request_sql_param,
        "out_put": out_put,
        "request_name": request_name
    }
    opsql.insert_sql(data)
    opsql.close()