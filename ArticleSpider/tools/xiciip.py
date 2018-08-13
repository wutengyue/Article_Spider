# # -*- coding: utf-8 -*-
import requests
# from scrapy.selector import Selector
# import pymysql
#
# conn = pymysql.connect(host='127.0.0.1', user="root", passwd="521hhxx", db="spiders", charset="utf8")
# cursor = conn.cursor()
#
#
# def crawl_ips():
#     #爬取西刺的免费ip代理
#     headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
#     count = 0
#     for i in range(2000, 3353):
#         print(i)
#         url = "http://www.xicidaili.com/nn/{}".format(i+1)
#         print(url)
#         re = requests.get("http://www.xicidaili.com/nn/{}".format(i+1), headers=headers)
#
#         selector = Selector(text=re.text)
#         all_trs = selector.css("#ip_list tr")
#
#         ip_list = []
#         for tr in all_trs[1:]:
#             speed_str = tr.css(".bar::attr(title)").extract()[0]
#             if speed_str:
#                 speed = float(speed_str.split("秒")[0])
#             all_texts = tr.css("td::text").extract()
#
#             ip = all_texts[0]
#             port = all_texts[1]
#             proxy_type = all_texts[5]
#             if 'HTTP' in proxy_type:
#                 print('HTTP in...')
#                 ip_list.append((ip, port, speed, proxy_type))
#
#         for ip_info in ip_list:
#             cursor.execute(
#                 "insert xiciip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, '{3}')".format(
#                     ip_info[0], ip_info[1], ip_info[2], ip_info[3]
#                 )
#             )
#
#             conn.commit()
#             count += 1
#             print(count)


class GetIP(object):
    # def delete_ip(self, ip):
    #     #从数据库中删除无效的ip
    #     delete_sql = """
    #         delete from xiciip where ip='{0}'
    #     """.format(ip)
    #     cursor.execute(delete_sql)
    #     conn.commit()
    #     return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                'http': proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            # self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                # self.delete_ip(ip)
                return False


    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        # random_sql = """
        #       SELECT ip, port, proxy_type FROM xiciip
        #       where proxy_type = 'HTTPS'
        #       and ip = '106.56.102.219'
        #       ORDER BY RAND()
        #       LIMIT 1
        #     """
        # result = cursor.execute(random_sql)

        # for ip_info in cursor.fetchall():
        #     ip = ip_info[0]
        #     port = ip_info[1]
        #     proxy_type = ip_info[2]

        # 使用蘑菇代理API获取一个ip
        r = requests.get(
            'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=7c6fed29599d4cfdbfd694b3df7e1e3f&count=1&expiryDate=0&format=1&newLine=2'
        )

        ip_text = eval(r.text)  # r.text返回字符串'{"code":"0","msg":[{"port":"48197","ip":"123.162.84.205"}]}'，eval将其转换为字典

        port = ip_text['msg'][0]['port']
        ip = ip_text['msg'][0]['ip']

        judge_re = self.judge_ip(ip, port)
        print('judge_re: {}'.format(judge_re))
        if judge_re:
            proxy = "http://{0}:{1}".format(ip, port)
            print(proxy)
            return proxy
        else:
            return self.get_random_ip()



# if __name__ == "__main__":
#     # get_ip = GetIP()
#     # get_ip.get_random_ip()
#     crawl_ips()
