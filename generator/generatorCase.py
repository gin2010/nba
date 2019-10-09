# -*- coding: utf-8 -*-
# @Date : 2019/09/27
# @Author : water
# @Version  : v1.0
# @Desc  :自动生成单个字段的测试用例、根据excel表中的字段生成联合字段的测试用例及测试主流程


import json,logging,xlrd,random,
import configparser

#日志配置
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Generator(object):

    def __init__(self):
        #加载配置文件中的内容
        config = configparser.ConfigParser()
        config.read('generator.ini')  # 读取文件


    def _read_excel(self,path):
        '''
        读取用例excel中的数据
        :param path:
        :return:
        '''
        pass


    def _random_string(self,sort,minlen,maxlen):
        '''
        根据单个字段类型及长度区间，生成对应的值
        :param sort:
        :param minlen:
        :param maxlen:
        :return:
        '''
        pass


    def _connect_sql(self):
        '''
        连接数据库
        :return:
        '''
        pass


    def _update_temp(self,temp,datas):
        '''
        使用读取的datas来更新temp模板里对应key的value
        :param temp:
        :param datas:
        :return:
        '''
        return temp


    def generate_single_case(self):
        '''
        生成单个字段的测试用例
        :return:
        '''
        pass


    def generate_multiple_case(self):
        '''
        生成联合字段与主流程的测试用例
        :return:
        '''
        pass


if __name__ =="__main__":
