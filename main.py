# 调试爬虫

from scrapy.cmdline import execute

import sys
import os

# 获取main.py文件所在目录
# mainpy_dir = os.path.dirname(os.path.abspath(__file__))
#
# sys.path.append(mainpy_dir)

# execute(['scrapy', 'crawl', 'taobao'])
print('run spider')
execute(['scrapy', 'crawl', 'jobbole'])
