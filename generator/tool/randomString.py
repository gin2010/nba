# -*- coding: utf-8 -*-
# @Date : 2019-8-28
# @Author : water
# @Desc  :实现传入字符类型与长度，返回固定长度的字符
# @Version  : v0.1


import random
import string
import os,time
import logging
from tool.randomCount import random_count

#日志配置
logging.basicConfig(level = logging.WARN,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class GetString:

    # 初始化并加载所有的strings
    def __init__(self):
        self.tool_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(os.path.dirname(self.tool_path),"data")
        chinese_path = os.path.join(self.data_path, 'chinese.config')
        fanti_path = os.path.join(self.data_path, 'fanti.config')
        nanti_path = os.path.join(self.data_path, 'nanti.config')
        #加载常用汉字
        f1 = open(chinese_path, 'r', encoding='UTF-8')
        self.chineses = f1.readline().replace(' ','')
        # logger.info(self.chineses[:10])
        logger.info("chinese is ok")
        f1.close()
        #加载常用繁体字
        f2 = open(fanti_path, 'r', encoding='UTF-8')
        self.fantis = f2.readline()
        # logger.info(self.fantis[1:2])
        logger.info("fantizi is ok")
        f2.close()
        #加载常用难检字
        f3 = open(nanti_path, 'r', encoding='UTF-8')
        self.nantis = f3.readline()
        # logger.info(self.nantis[1:10])
        logger.info("nantizi is ok")
        f3.close()
        #加载数字
        self.numbers = string.digits
        # logger.info(self.numbers)
        logger.info("number is ok")
        #加载全角数字
        self.qj_numbers = "０１２３４５６７８９"
        # logger.info(self.qj_numbers)
        logger.info("quanjiao number is ok")
        #加载小写字母
        self.lower_alphabet = string.ascii_lowercase
        # logger.info(self.lower_alphabet)
        logger.info("lower alphabet is ok")
        #加载大写字母
        self.upper_alphabet = string.ascii_uppercase
        # logger.info(self.upper_alphabet)
        logger.info("upper alphabet is ok")
        #加载大小写字母
        self.all_alphabet = string.ascii_letters
        # logger.info(self.all_alphabet)
        logger.info("all alphabet is ok")
        #加载特殊特号
        self.symbols = string.punctuation
        # logger.info(self.symbols)
        logger.info("symbol is ok")
        self.strings = list()


    # #按length生成相应长度的string
    # def random_string(self,length):
    #     self.result = random.choices(self.all_alphabet,k=length)
    #     logger.warning(self.result)


    #按length与类型生成相应长度的string
    def random_string_multiple(self,sort,length):
        results = ""
        sort_count = random_count(sort,length)
        logger.info(sort_count)
        # 添加数字
        result = random.choices(self.numbers,k=sort_count.get('SZ',0))
        # 添加大写字母
        result.extend(random.choices(self.upper_alphabet,k=sort_count.get('ZMD',0)))
        # 添加小写字母
        result.extend(random.choices(self.lower_alphabet,k=sort_count.get('ZMX',0)))
        # 添加汉字
        result.extend(random.choices(self.chineses,k=sort_count.get('HZ',0)))
        # 添加难体
        result.extend(random.choices(self.nantis,k=sort_count.get('NT',0)))
        # 添加繁体
        result.extend(random.choices(self.fantis,k=sort_count.get('FT',0)))
        # 添加特殊符号
        result.extend(random.choices(self.fantis, k=sort_count.get('FH', 0)))
        # 添加全角数字
        result.extend(random.choices(self.qj_numbers, k=sort_count.get('QJSZ', 0)))
        # 打乱顺序
        random.shuffle(result)
        results = "".join(result)
        return results

    # 按位置生成小数、浮点类型
    def random_int_and_double(self,ninteger=1,ndigit=0):

        results = round(random.random() + random.randint(1,10**ninteger-1),ndigit)
        return results

    # 生成日期："2019-08-11 14:17:39"
    def random_datetime(self,start_year,end_year):
        a1 = (start_year, 1, 1, 0, 0, 0, 0, 0, 0)
        a2 = (end_year, 12, 31, 23, 59, 59, 0, 0, 0)
        start = time.mktime(a1)
        end = time.mktime(a2)
        t = random.randint(start, end)
        date_touple = time.localtime(t)
        result = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
        return result


    # 针对纳税人识别号不同位数不同类型进行单独生成
    def random_string_nsrsbh(self, sort, length):
        pass


if __name__=="__main__":

    get_string = GetString()
    # results = get_string.random_string_multiple(["QJSZ","SZ","ZMX","ZMD","FT"],20)
    # print(results)
    # get_string.random_int_and_double(2)
