import uuid
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pokemonspider.items import PokemonItem

class PokemonSpider(CrawlSpider):
    name = "pokemon"
    allowed_domains = ["www.pokemon.com"]
    start_urls = ["https://www.pokemon.com/us/api/pokedex"]
    base_url = "https://www.pokemon.com/us/api/pokedex"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    }

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
        "pokemonspider.pipelines.MongoPokedexPipeline": 301,
        },
    }

    def start_requests(self):
        url = self.base_url
        yield Request(url, callback=self.parse_item, headers=self.headers)


    def parse_item(self, response):
        # 将JSON响应转换为Python字典
        dataset = response.json()
        for data in dataset:
            # 创建一个新的PokemonItem实例
            item = PokemonItem()
            # 从JSON数据填充Item字段
            item['number'] = data.get('number')
            item['name'] = data.get('name')
            item['slug'] = data.get('slug')
            item['detail_page_url'] = data.get('detailPageURL')
            item['thumbnail_alt_text'] = data.get('ThumbnailAltText')
            item['thumbnail_image'] = data.get('ThumbnailImage').replace(" ", "")  # 移除URL中的空格
            item['type'] = data.get('type')
            item['abilities'] = data.get('abilities')
            item['weakness'] = data.get('weakness')
            item['weight'] = data.get('weight')
            item['height'] = data.get('height')
            item['featured'] = data.get('featured') == "true"  # 将字符串'true'转换为布尔值
            item['collectibles_slug'] = data.get('collectibles_slug')
            item['id'] = data.get('id')

            # 返回填充后的Item
            yield item