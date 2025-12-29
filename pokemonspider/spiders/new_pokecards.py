import re
import uuid
from typing import Iterable
import pymongo
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pokemonspider.items import PokemonItem
from pokemonspider.settings import MONGO_URL, MONGO_DATABASE


# https://wiki.52poke.com/wiki/宝可梦集换式卡牌游戏列表#第七世代_2
class PokeCardspider(CrawlSpider):
    name = "pokecards"
    allowed_domains = ["wiki.52poke.com"]
    # URL中文转码
    start_urls = ["https://wiki.52poke.com/wiki/"]
    base_url = "https://wiki.52poke.com/wiki/"

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
        "pokemonspider.pipelines.MongoCardsPipeline": 301,
        },
    #     'DOWNLOADER_MIDDLEWARES':{
    #     'scrapy_proxies.RandomProxy': 100,
    #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # },
    #     'SPIDER_MIDDLEWARES' :{
    #     'pokemonspider.middlewares.CookieMiddleware': 543,
    #  }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    }

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
        "pokemonspider.pipelines.MongoPokedexPipeline": 301,
        },
    }

    def __init__(self, *args, **kwargs):
        super(PokeCardspider, self).__init__(*args, **kwargs)
        # 连接到MongoDB
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DATABASE]

    def start_requests(self):
        # #从Pokemon的库里取名字，构成初始页面
        # items = self.db[MONGO_COLLECTION].distinct(self.item_field)
        items = ['宝可梦集换式卡牌游戏列表#第七世代_2', '宝可梦集换式卡牌游戏列表#第八世代_2', '宝可梦集换式卡牌游戏列表#第九世代_2']

        # 使用列表推导式生成所有初始请求
        requests = [
            Request(
                url=self.base_url + f'{item}',
                callback=self.parse_index,
                priority=0
            )
            for item in items
        ]
        # 发送请求
        yield from requests

        # #测试
        # yield Request(
        #         url="https://limitlesstcg.com/cards?q=pokemon:Zamazenta",
        #         callback=self.parse_index,
        #         dont_filter=True,
        #         priority=0
        #     )

    def parse_index(self, response):
        domain = "https://wiki.52poke.com"
        # print(response.text)
        # 提取所有简中系列的卡牌链接
    #     roundy bg-UM b-US - 第七代
    #     roundy bg-冠之雪原 bd-铠之孤岛 - 第八代
    #     roundy bgl-紫 b-朱 - 第九代

        cards_index = response.css('''
            table.roundy.bg-UM.b-US,
            table.roundy.bg-冠之雪原.bd-铠之孤岛, 
            table.roundy.bgl-紫.b-朱
        ''').css('tr:nth-child(n+2) a:not([href^="/wiki/File:"])::attr(href)').getall()
        print(cards_index)

        for card_url in cards_index:
            card_url = domain + card_url
            # yield Request(card_url, callback=self.parse_card_item)
            print(card_url)
            # yield Request(card_url, callback=self.parse_card_series)

        #测试
        yield Request(
                url="https://wiki.52poke.com/wiki/%E5%88%A9%E5%88%83%E7%8C%9B%E9%86%92%EF%BC%88TCG%EF%BC%89",
                callback=self.parse_card_series,
                dont_filter=True,
                priority=0
            )

    def parse_card_series(self, response):

        # 方法1：使用ID精确查找
        cards_data = response.xpath('''
                //span[@id="卡牌列表"]/ancestor::h2/following-sibling::table[1]//tr[td]
            ''')

        cards_list = []
        for row in cards_data:
            # 跳过空行或无效行
            if len(row.xpath('./td')) < 4:
                continue
            # print(row)
            card_info = {
                'number': row.xpath('./td[1]//text()').get('').strip(),
                'name': row.xpath('./td[2]//a[not(contains(@href, "File:"))]/text()').get('').strip(),
                'url': row.xpath('./td[2]//a[not(contains(@href, "File:"))]/@href').get(),
                'title': row.xpath('./td[2]//a[not(contains(@href, "File:"))]/@title').get(),
                'attribute': self.extract_attribute(row.xpath('./td[3]')),
                'rarity': self.extract_rarity(row.xpath('./td[4]')),
            }

            # 验证必要字段
            if card_info['url'] and card_info['name'] and card_info['number']:
                cards_list.append(card_info)
        print(cards_list)
        print(f"在{response.url}中找到{len(cards_list)}张卡牌")
        # return cards_list



    # def parse_item(self, response):
    #     # 将JSON响应转换为Python字典
    #     dataset = response.json()
    #     for data in dataset:
    #         # 创建一个新的PokemonItem实例
    #         item = PokemonItem()
    #         # 从JSON数据填充Item字段
    #         item['number'] = data.get('number')
    #         item['name'] = data.get('name')
    #         item['slug'] = data.get('slug')
    #         item['detail_page_url'] = data.get('detailPageURL')
    #         item['thumbnail_alt_text'] = data.get('ThumbnailAltText')
    #         item['thumbnail_image'] = data.get('ThumbnailImage').replace(" ", "")  # 移除URL中的空格
    #         item['type'] = data.get('type')
    #         item['abilities'] = data.get('abilities')
    #         item['weakness'] = data.get('weakness')
    #         item['weight'] = data.get('weight')
    #         item['height'] = data.get('height')
    #         item['featured'] = data.get('featured') == "true"  # 将字符串'true'转换为布尔值
    #         item['collectibles_slug'] = data.get('collectibles_slug')
    #         item['id'] = data.get('id')
    #
    #         # 返回填充后的Item
    #         yield item




    def extract_attribute(self, td_element):
        """提取属性信息"""
        # 尝试从图片alt属性提取
        attribute = td_element.xpath('.//img/@alt').get()
        if attribute:
            return attribute

        # 尝试从文本提取
        attribute = td_element.xpath('.//text()').get('').strip()
        return attribute if attribute else '未知'

    def extract_rarity(self, td_element):
        """提取稀有度信息"""
        rarity = td_element.xpath('.//text()').get('').strip()
        # 清理稀有度文本
        if 'title="' in rarity:
            rarity = re.search(r'title="([^"]+)"', rarity).group(1) if re.search(r'title="([^"]+)"', rarity) else rarity
        return rarity