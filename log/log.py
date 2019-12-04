# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.0
# @Desc  :

import logging
from logging import handlers

logger = logging.getLogger("new.log")
fmt = '%(asctime)s -%(pathname)s[line:%(lineno)d] -%(levelname)s:%(message)s'
format_str = logging.Formatter(fmt)#设置日志格式
logger.setLevel(30)#设置日志级别

sh = logging.StreamHandler()#往屏幕上输出
sh.setFormatter(format_str) #设置屏幕上显示的格式
th = handlers.TimedRotatingFileHandler(filename="new.log",when='D',backupCount=3,encoding='utf-8')#
th.setFormatter(format_str)#设置文件里写入的格式
logger.addHandler(sh) #把对象加到logger里
logger.addHandler(th)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.critical("critical")
logger.error("error")

