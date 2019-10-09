# coding:utf-8
# author:water

import requests
import csv
import xlrd
xlrd.open_workbook()


def check_value(proxy):
    '''head 信息'''
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                 'Connection': 'keep-alive'}
    '''http://icanhazip.com会返回当前的IP地址'''
    p = requests.get('http://www.baidu.com', headers=head, proxies=proxy)
    if p.status_code ==200:
        print(proxy)


'''代理IP地址（高匿）'''
proxy = {}
with open("prox_ip.csv",'r') as f :
    ip_csv = csv.reader(f)
    for i in ip_csv:
        if i:
            proxy[i[0]] = i[0]+"://"+i[1] + ":" +i[2]
            check_value(proxy)

