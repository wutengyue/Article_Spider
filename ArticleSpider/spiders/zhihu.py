# # -*- coding: utf-8 -*-
# import scrapy
# import time
# import pickle
# import json
# import re
# from ArticleSpider.items import ZhihuTopicTopAnswersItem, ZhihuTopicTopAnswersItemLoader
# from scrapy.http import Request
# from selenium import webdriver
# import html
# import os
# from scrapy.selector import Selector
#
#
# class ZhihuSpider(scrapy.Spider):
#     name = 'zhihu'
#     allowed_domains = ['www.zhihu.com']
#     # start_urls为知乎某个话题的精华问题feed流的json数据
#     # start_urls = ['https://www.zhihu.com/api/v4/topics/{}/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit={}&offset={}']
#     start_urls = ['https://www.zhihu.com/topics#%E7%94%9F%E6%B4%BB%E6%96%B9%E5%BC%8F']
#
#     # 话题id
#     topic_id = 19553528
#     count = 0
#     headers = {
#         'HOST': 'www.zhihu.com',
#         'Referer': 'https://www.zhizhu.com',
#         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Mobile Safari/537.36'
#     }
#     print('---------------------------------')
#     print('---------------------------------')
#     # browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#     # browser.get('https://www.zhihu.com/signin')
#     # 输入用户名、密码，点击登录按钮
#     # browser.find_element_by_css_selector('.Login-content input[name="username"]').send_keys('17610831881')
#     # browser.find_element_by_css_selector('.Login-content input[name="password"]').send_keys('521hhxx@ZH')
#     # browser.find_element_by_css_selector('.Login-content .SignFlow-submitButton').click()
#
#     def get_cookies_by_local(self):  # 从本地获取cookies
#         cookies = {}
#         path = '/Users/wutengyue/Develop/ArticleSpider/cookies/zhihu/'
#         cookies_files = os.listdir(path)
#         for cookie_file in cookies_files:
#             if cookie_file.endswith('zhihu'):
#                 with open(path + cookie_file, 'rb') as f:
#                     cookie = pickle.load(f)
#                     cookie_name = cookie['name']
#                     cookie_value = cookie['value']
#                     cookies[cookie_name] = cookie_value
#
#         return cookies
#
#     def get_cookies_by_login(self):  # 登录后获取cookies
#         # 模拟登陆
#         # browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#         # 打开加载这个网页
#         self.browser.get('https://www.zhihu.com/signin')
#         # 输入用户名、密码
#         # browser.find_element_by_css_selector('.Login-content input[name="username"]').send_keys('17610831881')
#         # browser.find_element_by_css_selector('.Login-content input[name="password"]').send_keys('521hhxx@ZH')
#         # browser.find_element_by_css_selector('.Login-content .SignFlow-submitButton').click()
#         time.sleep(10)  # 暂停3s，获取cookie
#         cookies_login = self.browser.get_cookies()
#         print(cookies_login)
#         cookies = {}
#         for cookie in cookies_login:
#             # 写入文件
#             with open('/Users/wutengyue/Develop/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb') as f:
#                 pickle.dump(cookie, f)
#                 cookie_name = cookie['name']
#                 cookie_value = cookie['value']
#                 cookies[cookie_name] = cookie_value
#         time.sleep(3)
#         # browser.close()  # cookie写入文件后，5s后关闭浏览器
#
#         return cookies
#
#     def start_requests(self):
#         # cookies = ZhihuSpider.get_cookies_by_local()  # 获取cookies
#         cookies = ZhihuSpider.get_cookies_by_login(self)
#         # 传入请求头headers、cookies，模拟真人请求
#         # 不填入headers, Chrome模拟登陆知乎，会报400错误，不进入parse
#         # 使用meta将cookies传递给parse函数，使后面的处理函数能够带着cookies请求数据
#         # return [scrapy.Request(self.start_urls[0].format(self.topic_id, 10, 0), dont_filter=False, headers=self.headers, cookies=cookies, meta={'cookies': cookies})]
#         return [scrapy.Request(self.start_urls[0], dont_filter=False, headers=self.headers, cookies=cookies, meta={'cookies': cookies})]
#
#     def parse(self, response):  # start_request请求服务器成功后，会生成response返回给回调函数parse
#         cookies = response.meta.get('cookies')
#
#         text_file = response.text
#         with open('/Users/wutengyue/Downloads/text_file.txt', 'r') as f1:
#             f1.write(text_file)
#
#         content_file = response.content
#         with open('/Users/wutengyue/Downloads/content_file.txt', 'r') as f2:
#             f2.write(content_file)
#
#         feeds_json = json.loads(response.text)
#         is_end = feeds_json["paging"]["is_end"]
#         next_url = feeds_json["paging"]["next"]
#
#         q_url = 'https://www.zhihu.com/question/'
#
#         for feed in feeds_json['data']:
#             feed_dict = {}  # 将json数据接口中的数据，放到字典中，传给parse_q_url
#
#             feed_type = feed['target']['type']
#             if feed_type == 'article':
#                 continue
#             elif feed_type == 'answer':
#                 feed_dict['feed_type'] = feed_type  # feed type
#                 q_id = feed['target']['question']['id']  # question
#                 print(q_id)
#                 q_id_url = q_url + str(q_id)
#                 print(q_id_url)
#                 feed_dict['q_id'] = q_id
#                 feed_dict['q_title'] = feed['target']['question']['title']
#                 feed_dict['q_id_url'] = q_id_url
#                 feed_dict['q_created'] = feed['target']['question']['created']
#                 feed_dict['q_type'] = feed['target']['question']['type']
#                 feed_dict['q_question_type'] = feed['target']['question']['question_type']
#
#                 feed_dict['a_id'] = feed['target']['id']  # answer
#                 feed_dict['a_created_time'] = feed['target']['created_time']
#                 feed_dict['a_updated_time'] = feed['target']['updated_time']
#                 feed_dict['a_voteup_count'] = feed['target']['voteup_count']
#                 feed_dict['a_comment_count'] = feed['target']['comment_count']
#
#                 feed_dict['author_id'] = feed['target']['author']['id']  # author
#                 feed_dict['author_name'] = feed['target']['author']['name']
#                 feed_dict['author_url'] = feed['target']['author']['url']
#                 feed_dict['author_type'] = feed['target']['author']['type']
#                 feed_dict['author_headline'] = feed['target']['author']['headline']
#                 feed_dict['author_is_org'] = feed['target']['author']['is_org']
#                 feed_dict['author_gender'] = feed['target']['author']['gender']
#
#             yield Request(url=q_id_url, meta={'feed_dict': feed_dict}, headers=self.headers, cookies=cookies, callback=self.parse_q_url)
#         if not is_end:
#             yield scrapy.Request(next_url, headers=self.headers, cookies=cookies, callback=self.parse)
#
#     def parse_q_url(self, response):
#         url = response.url
#         self.browser.get(url)
#         selector = Selector(text=self.browser.page_source)
#         followers = selector.response.css('.QuestionHeader-follow-status strong::text').extract()
#
#         code = response.status  # debug用，看是否成功访问到response.url
#
#         html_text = html.unescape(response.text)  # 知乎html有转义，这里做下反转义，以便取值
#
#         # with open('/users/wutengyue/test.txt', 'wb') as f:  # html写入txt中，方便观察html结构、取值
#         #     f.write(htmlText.encode('utf8'))
#
#         q_views_ptn = '"visitCount":(\d+)'  # 取浏览数
#         q_views = re.search(q_views_ptn, html_text)
#         q_views = q_views.group(1)
#
#         q_followers_ptn = '(\d+),"collapsedAnswerCount"'  # 取关注人数
#         q_followers = re.search(q_followers_ptn, html_text)
#         q_followers = q_followers.group(1)
#
#         feed_dict = response.meta.get('feed_dict', '')  # 接收parse传来的dict
#         feed_item = ZhihuTopicTopAnswersItemLoader(item=ZhihuTopicTopAnswersItem(), response=response)
#
#         feed_item.add_value('feed_type', feed_dict['feed_type'])
#         feed_item.add_value('q_id', feed_dict['q_id'])  # question
#         feed_item.add_value('q_title', feed_dict['q_title'])
#         feed_item.add_value('q_id_url', feed_dict['q_id_url'])
#         feed_item.add_value('q_created', feed_dict['q_created'])
#         feed_item.add_value('q_views', q_views)
#         feed_item.add_value('q_followers', q_followers)
#         feed_item.add_value('q_question_type', feed_dict['q_question_type'])
#         feed_item.add_value('q_type', feed_dict['q_type'])
#
#         feed_item.add_value('a_id', feed_dict['a_id'])  # answer
#         feed_item.add_value('a_created_time', feed_dict['a_created_time'])
#         feed_item.add_value('a_updated_time', feed_dict['a_updated_time'])
#         feed_item.add_value('a_voteup_count', feed_dict['a_voteup_count'])
#         feed_item.add_value('a_comment_count', feed_dict['a_comment_count'])
#
#         feed_item.add_value('author_id', feed_dict['author_id'])
#         feed_item.add_value('author_name', feed_dict['author_name'])
#         feed_item.add_value('author_url', feed_dict['author_url'])
#         feed_item.add_value('author_type', feed_dict['author_type'])
#         feed_item.add_value('author_headline', feed_dict['author_headline'])
#         feed_item.add_value('author_is_org', feed_dict['author_is_org'])
#         feed_item.add_value('author_gender', feed_dict['author_gender'])
#
#         feed_item = feed_item.load_item()
#         yield feed_item
#
#         self.count = self.count + 1
#
#         print(self.count)
