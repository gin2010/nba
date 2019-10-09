# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class KdlPipeline(object):

    def __init__(self):
        self.f = open('prox_ip.csv', 'w')

    def process_item(self, item, spider):


        writer = csv.writer(self.f)
        writer.writerow((item['sort'], item['ip'], item['port']))
        return item

    def close_spider(self,spider):
        self.f.close()