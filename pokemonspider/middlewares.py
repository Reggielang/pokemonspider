# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from twisted.internet.defer import Deferred
from pyppeteer import launch
from scrapy.http import HtmlResponse
import asyncio
import logging
import requests

class PokemonspiderSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i



    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class PokemonspiderDownloaderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)

from scrapy.http import  HtmlResponse
from selenium import webdriver
import time
class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        url = request.url
        browser = webdriver.Edge()
        browser.get(url)
        time.sleep(7)
        html = browser.page_source
        return HtmlResponse(url=url, body=html, encoding='utf-8', request=request)


import random
import requests
from scrapy import signals
from scrapy.exceptions import IgnoreRequest


class CookieMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents
        self.cookies = None
        self.update_cookies()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings.get('USER_AGENTS'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        self.update_cookies()

    def update_cookies(self):
        try:
            response = requests.get('https://limitlesstcg.com/cards', headers={'User-Agent': random.choice(self.user_agents)})
            response.raise_for_status()
            self.cookies = dict(response.cookies)
            print("Updated cookies:", self.cookies)
        except requests.RequestException as e:
            print(f"Error fetching fresh cookies: {e}")

    def process_request(self, request, spider):
        if not self.cookies or 'Pardon Our Interruption' in request.meta.get('retry_times', 0):
            self.update_cookies()

        request.headers['cookies'] = self.cookies
        request.headers['User-Agent'] = random.choice(self.user_agents)
        print("cookies--------------",request.cookies)

    def process_response(self, request, response, spider):
        # 如果遇到403或特定文本，则认为cookie可能已失效，并尝试重新获取
        if response.status == 403 or 'Pardon Our Interruption' in response.text:
            self.update_cookies()
            new_request = request.replace(dont_filter=True)
            new_request.priority = request.priority + 1
            return new_request

        return response

    def process_exception(self, request, exception, spider):
        # 在这里可以处理任何异常情况，例如网络错误等
        print(f"Caught exception: {exception}")
        return None