# import time
# import pickle
# from selenium import webdriver
#
#
# def get_cookies_by_login():  # 登录后获取cookies
#     # 模拟登陆
#     browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#     # 打开加载这个网页
#     # browser.get('https://login.taobao.com/member/login.jhtml?spm=a230r.1.754894437.1.2c067960rnXPxF&f=top&redirectURL=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3Djmsolution%26imgfile%3D%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.2017.201856-taobao-item.1%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306%26sort%3Dsale-desc%26bcoffset%3D0%26p4ppushleft%3D%252C44%26s%3D0')
#     browser.get('https://login.taobao.com')
#     time.sleep(5)
#     # 输入用户名、密码
#     browser.find_element_by_css_selector('.Login-content input[name="username"]').send_keys('17610831881')
#     browser.find_element_by_css_selector('.Login-content input[name="password"]').send_keys('521hhxx')
#     browser.find_element_by_css_selector('.Login-content .SignFlow-submitButton').click()
#     time.sleep(3)  # 暂停5s，获取cookie
#     cookies_login = browser.get_cookies()
#     print(cookies_login)
#     cookies = {}
#     for cookie in cookies_login:
#         # 写入文件
#         with open('/Users/wutengyue/Develop/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb') as f:
#             pickle.dump(cookie, f)
#             cookie_name = cookie['name']
#             cookie_value = cookie['value']
#             cookies[cookie_name] = cookie_value
#     time.sleep(3)
#     browser.close()  # cookie写入文件后，5s后关闭浏览器
#
#     return cookies