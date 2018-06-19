# -*- coding: utf-8 -*-
import os, urllib3

import scrapy
import requests
import re

# from trc.items import MeizituSpiderItem
from trc.items import MeizituSpiderItem

next_page_link = []


# item = {}
# def download(url):
#     file_name = url[-18:]
#     path = "E:\study\python进阶\meizitus_spider\meizitu"
#     name = os.path.join(path, file_name.replace('/', '_'))
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'}
#     if not os.path.exists(name):
#         r = requests.get(url, headers=headers)
#         with open(name, 'wb') as f:
#             f.write(r.content)
#     else:
#         print("this pic exists error...")


class MeizituDemoSpider(scrapy.Spider):
    name = 'meizitu_demo'
    download_delay = 1
    allowed_domains = ['meizitu.com']
    # allow_urls = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
        for i in response.xpath("//div[@class = 'pic']/a/@href").extract():
            yield scrapy.Request(i, callback=self.parse_picture)
        pages_link = response.xpath("//div[@id = 'wp_page_numbers']/ul/li/a/@href").extract()
        full_page_link = "http://www.meizitu.com/a/" + pages_link[0]
        if full_page_link not in next_page_link:
            yield scrapy.Request(full_page_link, callback=self.parse)
        else:
            print("I finished but i can't error....")

    def parse_picture(self, response):
        item = MeizituSpiderItem()
        pic_name = response.selector.xpath("//div[@class='metaRight']/h2/a/text()").extract()
        pic_url = response.selector.xpath("//div[@id='picture']/p/img/@src").extract()
        item['pic_name'] = pic_name
        item['pic_url'] = pic_url
        yield item

        # for url in item['pic_url']:
        # download(url)
        # for name in item['pic_name']:
        #     print(re.findall("[\u4e00-\u9fa5]", name))
