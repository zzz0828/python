# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors


class TrcPipeline(object):
    def process_item(self, item, spider):
        self.db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='meizitu', port=3306,
                                  charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        self.cursor.execute("insert into mzt(name, pic_url) value(%s, %s) ", (item['pic_name'][0], item['pic_url'][0]))

        return ""
