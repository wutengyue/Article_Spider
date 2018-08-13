# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleIterm, ArticleItemLoader
from ArticleSpider.utils.common import strURL_to_md5
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # start_urls = ['https://httpbin.org/get']
    # start_urls = ['https://detail.tmall.com/item.htm?spm=a230r.1.14.7.56116fbeiDBOtk&id=558550356564&cm_id=140105335569ed55e27b&abbucket=10&sku_properties=10004:709990523;5919063:6536025;12304035:3222911']

    # 生成全局的browser
    # def __init__(self):
    #     # 设置无界面启动Chrome
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')
    #     self.browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options)
    #     # 重写了init方法，这里要调用、启用一下父类的init方法
    #     super().__init__()
    #     # 爬虫关闭时，推出浏览器
    #     dispatcher.connect(self.spider_close, signals.spider_closed)
    #
    # def spider_close(self, spider):
    #     print('spider closed, quit browser!')
    #     self.browser.quit()

    def parse(self, response):
        # 获取文章列表中的文章url，并交给scrapy下载、解析
        # 获取下一页的url并交给scrapy下载，下载完成后交给parse

        # 获取文章列表中的文章url，并交给scrapy下载、解析
        # post_urls = response.xpath('//*[@id="archive"]//div[@class="post-thumb"]/a/@href').extract()
        # post_urls = response.xpath('//*[@id="archive"]//div[@class="post-meta"]/p/a[1]/@href').extract()
        text = response.text
        nodes_a = response.css('#archive .post-thumb a')

        for node_a in nodes_a:
            article_url = nodes_a.css('::attr(href)').extract_first()
            article_url = parse.urljoin(response.url, article_url)

            cover_img_url = node_a.css('img::attr(src)').extract_first()
            cover_img_url = parse.urljoin(response.url, cover_img_url)

            yield Request(url=article_url, meta={'cover_img_url': cover_img_url}, callback=self.parse_details)
            # yield Request(post_url, callback=self.parse_details)

        # 获取下一页的url并交给scrapy下载，下载完成后交给parse
        # next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_details(self, response):
        metas = response.meta
        print(metas)
        # 实例化iterm
        article_iterm = JobBoleArticleIterm()

        #parse_details函数用于提取文章的具体字段


        # # title = response.xpath('//*[@id="post-110287"]/div[1]/h1')
        # title = response.css('.entry-header h1::text').extract_first()
        #
        # # published_date_selector = response.xpath('//*[@id="post-110287"]/div[2]/p/text()[1]')
        # published_date_selector = response.css('.entry-meta-hide-on-mobile::text').extract_first()
        # published_date = re.match('\\s+.*?(\d.*\d).*', published_date_selector).group(1)
        #
        # # like_nums = response.xpath('//*[@id="110287votetotal"]/text()').extract_first()
        # # like_nums = response.css('.post-adds h10::text').extract_first()
        # like_nums = response.css('.vote-post-up h10::text').extract_first()
        # match_like_nums = re.match('.*?(\d+).*', like_nums)
        # if match_like_nums:
        #     like_nums = int(match_like_nums.group(1))
        # else:
        #     like_nums = 0
        #
        # # collect_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/span[2]/text()').extract_first()
        # collect_nums = response.css('.bookmark-btn::text').extract_first()
        # match_collect_nums = re.match('.*?(\d+).*', collect_nums)
        # if match_collect_nums:
        #     collect_nums = int(match_collect_nums.group(1))
        # else:
        #     collect_nums = 0
        #
        # # comment_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/a/span/text()').extract_first()
        # comment_nums = response.css('.post-adds a span::text').extract_first()
        # match_comment_nums = re.match('.*?(\d+).*', comment_nums)
        # if match_comment_nums:
        #     comment_nums = int(match_comment_nums.group(1))
        # else:
        #     comment_nums = 0
        #
        # # content = response.xpath('//*[@id="post-110287"]/div[3]').extract_first()
        # content = response.css('.entry').extract_first()
        #
        # tags_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tags_list = [i for i in tags_list if not i.strip().endswith('评论')]
        # #或 tags_list = [i for i in tags_list if not re.match('.*评论.*', i)]
        # tags = ','.join(tags_list)
        #
        # article_iterm['title'] = title
        # try:
        #     published_date = datetime.datetime.strptime(published_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     published_date = datetime.datetime.strptime('1994/09/21', '%Y/%m/%d').date()
        # article_iterm['published_date'] = published_date
        # article_iterm['article_url'] = article_url
        # article_iterm['article_url_id'] = article_url_id
        # article_iterm['cover_image_url'] = [cover_img_url]
        # article_iterm['like_nums'] = like_nums
        # article_iterm['collect_nums'] = collect_nums
        # article_iterm['comment_nums'] = comment_nums
        # article_iterm['content'] = content
        # article_iterm['tags'] = tags

        # 通过item loader加载item

        article_url = response.url
        article_url_id = strURL_to_md5(article_url)
        cover_img_url = response.meta.get('cover_img_url', '')  #  文章封面, meta 字典类型，这里用了get方法,默认如果是空，则为'',不会报错

        iterm_loader = ArticleItemLoader(item=JobBoleArticleIterm(), response=response)  # 实例化一个ItemLoader
        iterm_loader.add_css('title', '.entry-header h1::text')
        iterm_loader.add_value('article_url', article_url)
        iterm_loader.add_value('article_url_id', article_url_id)
        iterm_loader.add_css('published_date', '.entry-meta-hide-on-mobile::text')
        iterm_loader.add_value('cover_image_url', [cover_img_url])
        iterm_loader.add_css('like_nums', '.vote-post-up h10::text')
        iterm_loader.add_css('collect_nums', '.bookmark-btn::text')
        iterm_loader.add_css('comment_nums', '.post-adds a span::text')
        iterm_loader.add_css('content', '.entry')
        iterm_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')

        article_iterm = iterm_loader.load_item()

        yield article_iterm
