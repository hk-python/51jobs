# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from logging import getLogger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time


class QcwySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QcwyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeleniumMiddleware(object):
    def __init__(self,timeout=None):
        self.logger=getLogger(__name__)
        self.timeout=timeout
        self.chrome_options = Options()
        self.browser=webdriver.Chrome()
        self.browser.set_window_size(1400,700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait=WebDriverWait(self.browser,self.timeout)

    def __del__(self):
        self.browser.close()


    def process_request(self,request,spider):
        KEYWORD = 'python'
        print('请求链接',request.url)
        self.logger.debug('Chrome is Starting')
        self.browser.get(request.url)  # 打开浏览器输入网址
        if request.url=='https://www.51job.com/':  #如果打开的网页是首页就进行登陆，搜索，返回url，网页源码；否则直接返回url，网页源码

            try:
                '''
                login = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'body > div.content > div > div.ubox > div.sml.e_icon.radius_5 > div.abut_box > span.abut.showLogin')
                ))#等待并找到登录按钮
                print('*****************************************************')
                login.click()  # 点击登录
                time.sleep(1)

                username = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#loginname')
                ))#等待账号输入框出现
                pwd = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#password')
                ))#等待密码输入框出现
                username.send_keys("******")#输入账号
                time.sleep(0.5)
                pwd.send_keys("******")#输入密码
                time.sleep(0.6)
                sub = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#login_btn')
                ))#等找到确认登录按钮
                sub.click()
                '''
                #若要模拟登陆，请放开'''  '''里的代码
                
                time.sleep(1)
                sou = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#kwdselectid')
                ))#找到搜索框
                di = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#work_position_input')
                ))#找到地区选择按钮

                sousub = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'body > div.content > div > div.fltr.radius_5 > div > button')
                ))#找到搜索按钮
                sou.send_keys(KEYWORD)#输入搜索条件
                time.sleep(1)
                di.click()
                time.sleep(0.5)
                dis = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.ttag')
                ))#地区选择选择全国
                dis.click()
                dissub = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#work_position_click_bottom_save')
                ))#确定地区
                dissub.click()
                time.sleep(1)
                sousub.click()
                time.sleep(5)
                return HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8',status=200) #返回url，网页源码
            except TimeoutException:
                return HtmlResponse(url=request.url,body=self.browser.page_source,status=500,request=request,encoding='utf-8')
        else:
            return HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
                   # service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
