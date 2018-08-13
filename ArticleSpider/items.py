# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re
import datetime
from scrapy.loader import ItemLoader


# date_convert方法默认会遍历每一个value即published_date，获取日期并转换成date格式
def date_convert(value):
    value = re.match('\\s+.*?(\d.*\d).*', value)
    if value:  # 如果匹配到了日期，就执行操作
        try:
            published_date = datetime.datetime.strptime(value.group(1), '%Y/%m/%d').date()
        except Exception as e:
            published_date = datetime.datetime.strptime('1994/09/21', '%Y/%m/%d').date()
        return published_date


# 通过正则获取字符串中的数字
def get_nums(value):
    value = re.match('.*?(\d+).*', value)
    if value:
        value = int(value.group(1))
    else:
        value = 0
    return value


# 去除tags中的'评论'
def get_tags(value):
    if '评论' not in value:  # 判断str2是否包含str1：if str1 in str2
        return value


# 重写output_processor，覆盖掉类ArticleItemLoader中default_output_processor = TakeFirst()，使其返回list
def return_value(value):
    return value

# 这个类应该是没用了，注释掉，不先删
# class ArticlespiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class ArticleItemLoader(ItemLoader):
    # 继承并重写ItemLoader的output_processor，使其输出['str']列表变为'str'字符串
    default_output_processor = TakeFirst()  # TakeFirst()，str格式返回list中第一个元素


class JobBoleArticleIterm(scrapy.Item):
    title = scrapy.Field()
    # 不做处理的情况下，ItemLoader返回list，一行是一个元素，即一行是一个published_date；
    published_date = scrapy.Field(
        input_processor=MapCompose(date_convert)  # 重写published_date的输入方法，即重写input_processor：使用MapCompose接收自定义方法date_convert处理日期
    )
    article_url = scrapy.Field()
    article_url_id = scrapy.Field()
    cover_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)  # 重写cover_image_url的输出方法，即重写output_processor：使用'MapCompose'+'return_value'接收list，然后原样返回list
    )
    cover_image_path = scrapy.Field()
    like_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    collect_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(get_tags),
        output_processor=Join(',')
    )


def unix_to_datatime(value):
    value = datetime.datetime.fromtimestamp(value)
    return value


class ZhihuTopicTopAnswersItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ZhihuTopicTopAnswersItem(scrapy.Item):
    feed_type = scrapy.Field()
    q_title = scrapy.Field()
    q_id = scrapy.Field()
    q_type = scrapy.Field()
    q_question_type = scrapy.Field()
    q_id_url = scrapy.Field()
    q_created = scrapy.Field(
        output_processor=MapCompose(unix_to_datatime)
    )
    q_followers = scrapy.Field()
    q_views = scrapy.Field()

    a_id = scrapy.Field()
    a_created_time = scrapy.Field(
        output_processor=MapCompose(unix_to_datatime)
    )
    a_updated_time = scrapy.Field(
        output_processor=MapCompose(unix_to_datatime)
    )
    a_voteup_count = scrapy.Field()
    a_comment_count = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    author_type = scrapy.Field()
    author_headline = scrapy.Field()
    author_is_org = scrapy.Field()
    author_gender = scrapy.Field()



