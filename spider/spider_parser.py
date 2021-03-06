# -*- coding: utf-8 -*-
import re

import time
from bs4 import BeautifulSoup
from pandas.io import json

from spider import spider_downloader
from spider.config_center import ConfigCenter


class SpiderParser(object):

    def __init__(self):
        self.downloader = spider_downloader.SpiderDownloader()

    def _get_product_info(self, item, html_cont):

        platform, skuid = item.split("_")
        soup = BeautifulSoup(html_cont, "html.parser")

        product_info = {}
        product_info['skuid'] = skuid
        product_info['platform'] = platform

        # 商品名称
        product_name = soup.find("div", id="itemInfo").find("div", id="name").h1.string
        product_info['name'] = product_name

        # 1级分类
        category1 = soup.find('a', clstag='shangpin|keycount|product|mbNav-1')
        product_info['category1'] = category1.get_text()

        # 2级分类
        category2 = soup.find('a', clstag='shangpin|keycount|product|mbNav-2')
        product_info['category2'] = category2.get_text()

        # 3级分类
        category3 = soup.find('a', clstag='shangpin|keycount|product|mbNav-3')
        product_info['category3'] = category3.get_text()

        # 4级分类
        category4 = soup.find('a', clstag='shangpin|keycount|product|mbNav-4')
        product_info['category4'] = category4.get_text()

        # 品牌id
        brand = re.findall(r"brand:(.+?),", soup.head.script.string)[0].encode('ascii','ignore').strip()
        product_info['brand'] = brand

        # 商品图片
        picture = re.findall(r"src: '(.+?)',", soup.head.script.string)[0]
        product_info['picture'] = picture

        return product_info

    def _get_product_price(self, html_cont_price):
        json_price = re.findall(r"\[(.+)\]", html_cont_price)[0]
        obj_price = json.loads(json_price)
        return obj_price

    def _get_product_comments(self, html_cont_comments):
        obj_comments = json.loads(html_cont_comments)
        return obj_comments

    def _get_resee(self, html_re_see):
        obj_re_see = json.loads(html_re_see)
        return obj_re_see

    def _get_new_items(self, obj_re_see):
        new_items = set()
        for datae in obj_re_see['data']:
            new_items.add(datae['sku'])
        return new_items

    def parse(self, item):
        # if item == "jd_1757862459" or item == "jd_1705471266" or item == "jd_1143324098" or item == "jd_1705471262" or item == "jd_1760490092":
        #     print "jd_1757862459"
        # 类似这些sku会转发到全球购 http://item.jd.hk/1705471266.html

        # 获取 url
        url_homepage = ConfigCenter.url_homepage(item)
        url_comment = ConfigCenter.url_comment(item)
        url_price = ConfigCenter.url_price(item)
        url_resee = ConfigCenter.url_resee(item)
        if url_homepage is None or url_comment is None or url_price is None or url_resee is None:
            return None

        # 获取正文
        urlback_homepage, htmlcont_homepage = self.downloader.get_html_cont(url_homepage)
        urlback_comments, htmlcont_comments = self.downloader.get_html_cont(url_comment)
        urlback_price, htmlcont_price = self.downloader.get_html_cont(url_price)
        urlback_resee, htmlcont_resee = self.downloader.get_html_cont(url_resee)
        if htmlcont_homepage is None or htmlcont_comments is None or htmlcont_price is None or htmlcont_resee is None:
            return None
        htmlcont_homepage = htmlcont_homepage.decode('gbk', 'ignore')
        htmlcont_resee = htmlcont_resee.decode('gbk', 'ignore')

        #判断是否全球购商品
        if urlback_homepage is None or urlback_homepage.find('item.jd.hk') != -1:
            print "[%s] item=%s 全球购商品,暂不处理." % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item)
            return None

        # 解析出 object
        index = 1
        try:
            p_info = self._get_product_info(item, htmlcont_homepage)
            index += 1
            p_price = self._get_product_price(htmlcont_price)
            index += 1
            p_comments = self._get_product_comments(htmlcont_comments)
            index += 1
            p_resee = self._get_resee(htmlcont_resee)
        except Exception as e:
            if index == 1:
                print "spider_parser.parse()._get_product_info()"
            if index == 2:
                print "spider_parser.parse()._get_product_price()"
                print "url:%s, html:%s" % (url_price, htmlcont_price)
            if index == 3:
                print "spider_parser.parse()._get_product_comments()"
            if index == 4:
                print "spider_parser.parse()._get_resee()"
            print "[%s] item=%s, %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item, e)
            # exstr = traceback.format_exc()
            # print exstr
            return None

        # 封装结果
        p_info['price_p'] = p_price['p'] # 现价
        p_info['price_m'] = p_price['m'] # 原价
        p_info['CommentsCount'] = p_comments['CommentsCount']  # 评价
        p_info['re_see_info'] = p_resee #看了又看信息

        return p_info


