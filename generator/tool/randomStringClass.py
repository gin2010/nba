# -*- coding: utf-8 -*-
# @Date : 2019-8-28
# @Author : water
# @Desc  :实现传入字符类型与长度，返回固定长度的字符
# @Version  : v0.1


import random,math,string,os,time
import logging

#日志配置
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GetString:

    # 初始化并加载所有的类型的全部strings
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"config")
        chinese_path = os.path.join(self.data_path, 'chinese.config')
        fanti_path = os.path.join(self.data_path, 'fanti.config')
        nanti_path = os.path.join(self.data_path, 'nanti.config')
        #加载常用汉字
        f1 = open(chinese_path, 'r', encoding='UTF-8')
        self.chineses = f1.readline().replace(' ','')
        # logger.debug(self.chineses[:10])
        logger.debug("chinese is ok")
        f1.close()
        #加载常用繁体字
        f2 = open(fanti_path, 'r', encoding='UTF-8')
        self.fantis = f2.readline()
        # logger.debug(self.fantis[1:2])
        logger.debug("fantizi is ok")
        f2.close()
        #加载常用难检字
        f3 = open(nanti_path, 'r', encoding='UTF-8')
        self.nantis = f3.readline()
        # logger.debug(self.nantis[1:10])
        logger.debug("nantizi is ok")
        f3.close()
        #加载数字
        self.numbers = string.digits
        # logger.debug(self.numbers)
        logger.debug("number is ok")
        #加载全角数字
        self.qj_numbers = "０１２３４５６７８９"
        # logger.debug(self.qj_numbers)
        logger.debug("quanjiao number is ok")
        #加载小写字母
        self.lower_alphabet = string.ascii_lowercase
        # logger.debug(self.lower_alphabet)
        logger.debug("lower alphabet is ok")
        #加载大写字母
        self.upper_alphabet = string.ascii_uppercase
        # logger.debug(self.upper_alphabet)
        logger.debug("upper alphabet is ok")
        #加载大小写字母
        self.all_alphabet = string.ascii_letters
        # logger.debug(self.all_alphabet)
        logger.debug("all alphabet is ok")
        #加载特殊特号
        self.symbols = string.punctuation
        # logger.debug(self.symbols)
        logger.debug("symbol is ok")
        self.strings = list()


    def _random_count(self,sort,length):
        """
        根据传入的sort列表中数据类型及总长度length，生成sort中每种数据类型的长度，合计长度 = length
        :param length:
        :return:
        """
        if length == len(sort):
            sort_count = dict()
            for i in range(len(sort)):
                sort_count[sort[i]] = 1
            return sort_count
        else:
            while True:
                sort_count = dict()
                for i in range(len(sort) - 1):
                    sort_count[sort[i]] = random.randint(1, length - len(sort))
                sort_count[sort[len(sort) - 1]] = length - sum(sort_count.values())
                if sort_count[sort[len(sort) - 1]] > 1:
                    break
            return sort_count


    def _random_string_multiple(self,sort,length):
        """
        按length与类型生成相应长度的string
        :param sort:输入的待测试字段的类型
        :param length:输入的待测试字段的长度
        :return:
        """
        results = ""
        sort_count = self._random_count(sort,length)
        logger.debug(sort_count)
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


    def _random_int_and_double(self,ninteger=1,ndigit=0):
        """
        按位置生成小数、浮点类型
        :param ninteger:
        :param ndigit:
        :return:
        """
        results = round(random.random() + random.randint(1,10**ninteger-1),ndigit)
        return results


    def _random_datetime(self,start_year,end_year):
        """
        生成日期："2019-08-11 14:17:39"
        :param start_year:
        :param end_year:
        :return:
        """
        a1 = (start_year, 1, 1, 0, 0, 0, 0, 0, 0)
        a2 = (end_year, 12, 31, 23, 59, 59, 0, 0, 0)
        start = time.mktime(a1)
        end = time.mktime(a2)
        t = random.randint(start, end)
        date_touple = time.localtime(t)
        result = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
        return result


    # 生成VARCHAR的通用测试用例
    def _varchar_case(self,length):
        length = int(length)
        results = list()
        # 1生成length位的数字
        results.append([f"生成{length}位的数字T", self._random_string_multiple(['SZ'], length)])
        # 2生成length+1位的数字
        results.append([f"生成{length+1}位的数字F", self._random_string_multiple(['SZ'], length + 1)])
        # 3生成length位的数字（两边有空格）
        results.append([f"生成{length}位的数字（两边有空格）T", "   " + self._random_string_multiple(['SZ'], length) + "  "])
        # 4生成length位的数字（中间有空格）
        result = self._random_string_multiple(['SZ'], length)
        results.append([f"生成{length}位的数字（中间有空格）F",
                        result[:math.floor(length / 2)] + "   " + result[math.floor(length / 2):length]])
        # 5生成length位的大写字母
        results.append([f"生成{length}位的大写字母T", self._random_string_multiple(['ZMD'], length)])
        # 6生成length+1位的大写字母
        results.append([f"生成{length+1}位的大写字母F", self._random_string_multiple(['ZMD'], length + 1)])
        # 7生成length位的小写字母
        results.append([f"生成{length}位的小写字母T", self._random_string_multiple(['ZMX'], length)])
        # 8生成length+1位的小写字母
        results.append([f"生成{length+1}位的小写字母F", self._random_string_multiple(['ZMX'], length + 1)])
        # 9生成length位的小写字母、数字
        if length >= 2:
            results.append([f"生成{length}位的小写字母、数字T", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 10生成length+1位的小写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length + 1)])
        # 11生成length位大写字母、数字
        if length >= 2:
            results.append([f"生成{length}位大写字母、数字T", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 12生成length+1位大写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length + 1)])
        # 13生成length位大小写字母、数字
        if length >= 3:
            results.append([f"生成{length}位大小写字母、数字T", self._random_string_multiple(['ZMD', 'ZMX', 'SZ'], length)])
        # 14生成length位全角数字
        results.append([f"生成{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 15生成length位大小写字母
        if length >= 2:
            results.append([f"生成{length}位大小写字母T", self._random_string_multiple(['ZMD', 'ZMX'], length)])
        # 16生成length位的汉字
        results.append([f"生成{length}位的汉字T", self._random_string_multiple(['HZ'], length)])
        # 17生成length+1位的汉字
        results.append([f"生成{length+1}位的汉字F", self._random_string_multiple(['HZ'], length + 1)])
        # 18生成length位的繁体字
        results.append([f"生成{length}位的繁体字T", self._random_string_multiple(['FT'], length)])
        # 19生成length位的难体字
        results.append([f"生成{length}位的难体字T", self._random_string_multiple(['NT'], length)])
        # 20生成length位的特殊符号
        results.append([f"生成{length}位的特殊符号T", self._random_string_multiple(['FH'], length)])
        # 21生成空值
        results.append(["生成空值F", ''])
        # 22生成null值
        results.append(["生成null值F", 'null'])
        # 23sql注入 "or"1"="1
        results.append(["sql注入F", self._random_string_multiple(['SZ'], length) + "''or''1''=''1"])
        # 24生成length-1位的数字
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的数字T", self._random_string_multiple(['SZ'], length - 1)])
        # 25生成length-1位的大写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的大写字母F", self._random_string_multiple(['ZMD'], length - 1)])
        # 26生成length-1位的小写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的小写字母F", self._random_string_multiple(['ZMX'], length - 1)])
        logger.info(results)
        return results


    # 针对纳税人识别号不同位数不同类型进行单独生成
    def random_string_nsrsbh(self, sort, length):
        pass


    def random_string_main(self,sort,length):
        if sort.strip().upper() == "VARCHAR":
            string_list = self._varchar_case(length)
            # [['生成11位的数字', '34140688517'], ['生成12位的数字', '031856900374']]
        elif sort.strip().upper() == "CHAR":
            string_list = self._char_case(length)
        elif sort.strip().upper() == "DATETIME":
            string_list = self._datetime_case()
        elif sort.strip().upper() == "INT":
            string_list = self._int_case(length)
        elif sort.strip().upper() == "DOUBLE":
            string_list = self._double_case(length)
        else:
            logger.error("输入的param_sort有误{}".format(d["param_sort"]))
        return string_list

if __name__=="__main__":

    get_string = GetString()
    # results = get_string._random_string_multiple(["QJSZ","SZ","ZMX","ZMD","FT"],20)
    # results = get_string._random_string_multiple(["SZ"], 1)
    results = get_string.random_string_main("VARCHAR",10)
    print(results)
    # get_string.random_int_and_double(2)
# if __name__ == "__main__":
#     sort_count = random_count(["SZ", "ZMX", "ZMD", "FT", "NT"], 100)
#     print(sort_count)
#     if sum(sort_count.values()) == 100:
#         print("right!!!")
#     # 测试length=1的情况
#     sort_count = random_count(["SZ"], 1)
#     print(sort_count)
#     # 测试length=2的情况
#     sort_count = random_count(["SZ"], 2)
#     print(sort_count)
#     # 测试length=2的情况
#     sort_count = random_count(["SZ", "ZMD"], 2)
#     print(sort_count)
#     # 测试length=3的情况
#     sort_count = random_count(["SZ", "ZMX", "ZMD"], 3)
#     print(sort_count)
#     # 测试length=3的情况
#     sort_count = random_count(["SZ", "ZMD"], 3)
#     print(sort_count)