# -*- coding: utf-8 -*-
import scrapy
from KDL.items import KdlItem
import time


class KdlSpider(scrapy.Spider):
    name = 'kdl'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/inha/1']
    MAXPAGE = 2

    def parse(self, response):
        datas = response.xpath("//tbody/tr")
        ips = KdlItem()
        for data in datas:
            ip = data.xpath("./td[@data-title='IP']/text()").extract()
            port = data.xpath("./td[@data-title='PORT']/text()").extract()
            sort = data.xpath("./td[@data-title='类型']/text()").extract()
            ips['ip'] = ip[0]
            ips['port'] = port[0]
            ips['sort'] = sort[0]
            yield ips

        for i in range(2,self.MAXPAGE):
            next_page = 'https://www.kuaidaili.com/free/inha/' + str(i)
            time.sleep(3)
            yield scrapy.Request(url=next_page, callback=self.parse)
