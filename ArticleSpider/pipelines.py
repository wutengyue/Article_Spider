# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 提取图片在本地的path
    # 同时需要修改settings.py
    def item_completed(self, results, item, info):
        # for (i, j) in results:
        #     cover_image_path = j['path']
        if 'cover_image_path' in item:

            cover_image_path = results[0][1]['path']

            item['cover_image_path'] = cover_image_path

            # 返回给另一个类ArticlespiderPipeline继续处理iterm
            return item


class JsonWithEncodingPipeline(object):
    # 自定义导出json文件
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy的JsonItemExporter方法，导出json文件
    def __init__(self):
        self.file = open('JsonExporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 采用同步的方法写入mysql
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "521hhxx", "article_spider", charset='utf8', use_unicode=True)
        self.cursor = self.db.cursor()
        # 写数据
    def process_item(self, item, spider):
        sql = """insert into article_jobbole(
                                              article_url_id, 
                                              title,
                                              published_date,
                                              article_url,
                                              cover_image_url,
                                              tags,
                                              like_nums,
                                              collect_nums,
                                              comment_nums,
                                              content
                                              )
                  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            item['article_url_id'],
            item['title'],
            item['published_date'],
            item['article_url'],
            item['cover_image_url'],
            item['tags'],
            item['like_nums'],
            item['collect_nums'],
            item['comment_nums'],
            item['content']
        ))
        self.db.commit()
        print('😃  😃  😃  😃  😃  😃')


class MysqlTwistedPipeline(object):
    # 初始化时接收一个dbpool实例
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 读取settings文件
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

        # 实例化一个dbpool
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted异步插入mysql
        query = self.dbpool.runInteraction(self.sql, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def sql(self, cursor, item):
        # 执行具体的插入
        sql = """insert into article_jobbole(
                                                      article_url_id, 
                                                      title,
                                                      published_date,
                                                      article_url,
                                                      cover_image_url,
                                                      tags,
                                                      like_nums,
                                                      collect_nums,
                                                      comment_nums,
                                                      content
                                                      )
                          values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        # 异步插入mysql，不可以使用self.cursor.execute，不然报没有cursor属性的错
        cursor.execute(sql, (
            item['article_url_id'],
            item['title'],
            item['published_date'],
            item['article_url'],
            item['cover_image_url'],
            item['tags'],
            item['like_nums'],
            item['collect_nums'],
            item['comment_nums'],
            item['content']
        ))


class ZhihuTopicIntoMysqlTwisted(object):
    # 初始化时接收一个dbpool实例
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 读取settings文件
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_DB_ZHIHU'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

        # 实例化一个dbpool
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted异步插入mysql
        query = self.dbpool.runInteraction(self.sql, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def sql(self, cursor, item):
        # 执行具体的插入
        sql = """insert into zhihu_topicfeed(
                                                      q_id
                                                      )
                          values (%s)
                """
        # 异步插入mysql，不可以使用self.cursor.execute，不然报没有cursor属性的错
        cursor.execute(sql, (
            item['q_id']
        ))
