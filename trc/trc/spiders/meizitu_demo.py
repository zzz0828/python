# -*- coding: utf-8 -*-
import os, urllib3

import scrapy

from trc.items import MeizituSpiderItem

next_page_link = []


class MeizituDemoSpider(scrapy.Spider):
    name = 'meizitu_demo'
    download_delay = 1
    allowed_domains = ['meizitu.com']
    # allow_urls = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
        # 获取当前页面所有的页面详情url
        for url in response.xpath("//div[@class = 'pic']/a/@href").extract():
            # 将获取的url传给parse_picture方法处理
            yield scrapy.Request(url, callback=self.parse_picture)
        # 获取每页的页码
        pages_link = response.xpath("//div[@id = 'wp_page_numbers']/ul/li/a/@href").extract()
        full_page_link = "http://www.meizitu.com/a/" + pages_link[0]
        if full_page_link not in next_page_link:
            next_page_link.append(full_page_link)
            # 将每页的url传给parse方法继续处理
            yield scrapy.Request(full_page_link, callback=self.parse)
        else:
            print("I finished but i can't error....")

    # 处理每个详情页的方法
    def parse_picture(self, response):
        item = MeizituSpiderItem()
        # 获取图片名字和图片的地址
        pic_name = response.selector.xpath("//div[@class='metaRight']/h2/a/text()").extract()
        pic_url = response.selector.xpath("//div[@id='picture']/p/img/@src").extract()
        item['pic_name'] = pic_name
        item['pic_url'] = pic_url
        yield item

        # 后面都是将图片保存到本地文件夹的代码，保存到数据库代码在pipelines.py文件
        # for url in item['pic_url']:
        # download(url)


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