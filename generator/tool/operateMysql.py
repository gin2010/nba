# -*- coding: utf-8 -*-
# File  : OperateMysql.py
# Author: water
# Date  : 2019/9/11
import pymysql
import logging

#程序运行日志配置
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# SQL_TEMPLATE = {
#     "case_id":case_id,
#     "step":step,
#     "test_desc":test_desc,
#     "step_reference":step_reference,
#     "http_method":http_method,
#     "headers":headers,
#     "url_sql":url_sql,
#     "request_sql_param":request_sql_param,
#     "out_put":out_put,
#     "request_name":request_name,
#     "aoto_replace":aoto_replace,
#     "expected_modify":expected_modify,
#     "expected_result":expected_result,
#     "expected_result_b":expected_result_b
#     }



def connet_sql():
    config = {
        "host":"127.0.0.1",
        "port":3306,
        "user":"root",
        "password":"root123456",
        "database":"demo1"
    }
    #连接数据库
    db = pymysql.connect(**config)
    #使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    return db,cursor


#关闭游标和数据库的连接
def close_sql(cursor):
    cursor.close()
    db.close()
    logger.warning("mysql closed!!")

def splice_sql():
    pass

def select_sql(cursor,table="step_data",**conditions):

    #使用execute()方法执行SQL语句
    cursor.execute("SELECT * FROM {0} where case_id = 24230000 and step = 2000;")
    #使用fetall()获取全部数据
    data = cursor.fetchall()
    #打印获取到的数据
    #print(data)
    return data

def insert_sql(db,cursor,data,table="step_data"):

    # 插入数据
    sql = '''INSERT INTO {} (case_id, step,test_desc,http_method,url_sql,out_put,request_sql_param,aoto_replace) VALUES ('{case_id}','{step}','{test_desc}','{http_method}','{url_sql}','{out_put}',"{request_sql_param}",'{aoto_replace}')'''
    sql = sql.format(table,**data)
    print(sql)
    cursor.execute(sql)
    db.commit()
    logger.warning(table,'成功插入', cursor.rowcount, '条数据')



if __name__ =="__main__":
    case_id =24230001
    step = 5
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
            "SGBZ": "1",
            "QDXMMC": "1232"}
    aoto_replace = 0
    data = {
        "case_id": case_id,
        "step": step,
        "test_desc": test_desc,
        "http_method": http_method,
        "url_sql": url_sql,
        "request_sql_param": request_sql_param,
        "out_put": out_put,
        "aoto_replace": aoto_replace
    }
    print(data)
    db,cursor = connet_sql()
    insert_sql(db,cursor,data)
    close_sql(cursor)