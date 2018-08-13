# from selenium import webdriver
# from scrapy.selector import Selector
# import time
#
# browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')  # executable_path=路径+driver名字
#
# # 打开并加载知乎登录页
# # browser.get('https://www.zhihu.com/signin')
# # time.sleep(3)
# # # 输入用户名、密码，点击登录按钮
# # browser.find_element_by_css_selector('.Login-content input[name="username"]').send_keys('17610831881')
# # time.sleep(3)
# # browser.find_element_by_css_selector('.Login-content input[name="password"]').send_keys('521hhxx@ZH')
# # time.sleep(3)
# # browser.find_element_by_css_selector('.Login-content .SignFlow-submitButton').click()
#
#
# # time.sleep(5)  # 暂停10s，获取cookie
# # Cookies = browser.get_cookies()
# # print(type(Cookies))
# # print(Cookies)
#
# # 打印该网页动态加载后的html
# # print(browser.page_source)
#
# #
# # t_selector = Selector(text=browser.page_source)
# # tm_price = t_selector.css('.tm-promo-price .tm-price::text').extract_first()
# # print(tm_price)
#
#
# # 访问需要抓去的知乎页面
# # browser.get('https://www.zhihu.com/question/24706380')
# #
# # print(browser.page_source)
# #
# # t_selector = Selector(text=browser.page_source)
# #
# # views = t_selector.css('.QuestionFollowStatus-counts strong::text').extract_first()
#
# # 淘宝登陆
# browser.get('https://login.taobao.com/member/login.jhtml?spm=a230r.1.754894437.1.2c067960rnXPxF&f=top&redirectURL=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3Djmsolution%26imgfile%3D%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.2017.201856-taobao-item.1%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306%26sort%3Dsale-desc%26bcoffset%3D0%26p4ppushleft%3D%252C44%26s%3D0')
# time.sleep(15)
# cookies_login = browser.get_cookies()
# print(cookies_login)
#
# browser.get("https://shopsearch.taobao.com/search?data-key=s&data-value=80&ajax=true&_ksTS=1533628232549_947&callback=jsonp948&app=shopsearch&q=%E7%BE%8E%E5%A6%86&imgfile=&commend=all&ssid=s5-e&search_type=shop&sourceId=tb.index&spm=a21bo.1000386.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&isb=0&shop_type=&ratesum=&s=60")
# cookies_login_json = browser.get_cookies()
# print(cookies_login_json)
# time.sleep(300)
# # # driver.find_element_by_xpath("//div[2]/div").click()
# # browser.find_element_by_link_text(u"亲，请登录").click()
# # time.sleep(3)
# # browser.find_element_by_id("J_Quick2Static").click()
# # time.sleep(3)
# # browser.find_element_by_id("TPL_username_1").send_keys("tb831421_55")
# # time.sleep(3)
# # browser.find_element_by_id("TPL_password_1").send_keys("bbmm521@#$")
# # time.sleep(10)
# # browser.find_element_by_id("J_SubmitStatic").click()
#
#
# # 淘宝商品列表页面
# # print(browser.page_source)
# # t_selector = Selector(text=browser.page_source)
# # shop = t_selector.css('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[2]/div[2]/div[3]/div[1]/a/span[2]')
# # print(shop)
# # time.sleep(10)
#
# browser.quit()
#
#
# if __name__ == '__main__':
#     pass